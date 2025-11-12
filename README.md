# Data Display Utility

This module provides helper functions to read a CSV file containing image paths and text labels, then render it as an interactive HTML table with embedded (base64-encoded) images.


---

## Installation

Install dependencies:

```
pip install pandas IPython pillow google-generativeai
```

These libraries are required for:

pandas — reading and processing CSV files  
IPython — rendering HTML content and displaying inline images  
pillow — loading and manipulating local image files (PIL)  
google-generativeai — accessing the Google AI Studio (Gemini) API for your prompt-based model testing



---

## 📂 Current File Structure

```
src/
└── ai_misko_asistentas/
    └── util/
        ├── __init__.py
        └── data_display.py
```

`data_display.py` — contains all logic for loading CSV files, validating structure, embedding images as base64, and displaying them in a rendered HTML table.  
`__init__.py` — marks the folder as a Python package so it can be imported.

Your dataset files should be stored in a parallel `data/` directory at the same level as `src/`:

```
data/
├── plant_examples.csv
└── example_images/
    ├── rubus_idaeus.jpg
    ├── amanita_muscaria.jpg
    ├── cantharellus_cibarius.jpg
    └── vaccinium_myrtillus.jpg
```

---

## Key Functionality

### show_data_table(csv_filename: str)
Main entry point — loads a CSV file, reads images, and displays them as an HTML table with thumbnails.

Automatically looks for the CSV under the project’s `data/` directory.

Requires columns:

- IMAGE_PATH — relative image paths (e.g., `example_images/file.jpg`)
- LATIN_NAME — text label for each image.

Uses base64 encoding so the images appear inline.

---

### Helper functions inside `data_display.py`

| Function | Description |
|-----------|-------------|
| resolve_csv_path(data_dir, csv_filename) | Validates that the given CSV file exists. |
| get_images_base_dir(csv_dir) | Determines where image paths should be resolved from (usually the same folder as the CSV). |
| load_csv(csv_path) | Loads the CSV file into a pandas DataFrame. |
| ensure_required_columns(df, required) | Checks that IMAGE_PATH and LATIN_NAME columns exist. |
| resolve_image_path(base_dir, path_str) | Builds a full path to each image, tolerating leading slashes /. |
| image_to_data_uri(img_path) | Reads and converts an image to a base64 data URI string. |
| to_img_tag(img_path, width) | Returns an HTML `<img>` tag string with embedded image data. |
| dataframe_with_inline_images(df, base_dir) | Builds a 2-column DataFrame (Image, Latin name) with inline images. |
| render_html_table(df) | Converts the DataFrame to HTML for display. |

---

## Example CSV

Example contents of `data/plant_examples.csv`:

```
IMAGE_PATH,LATIN_NAME
example_images/rubus_idaeus.jpg,rubus idaeus
example_images/amanita_muscaria.jpg,amanita muscaria
example_images/cantharellus_cibarius.jpg,cantharellus cibarius
example_images/vaccinium_myrtillus.jpg,vaccinium myrtillus
```

---

## Example Usage

Run this inside a notebook or Python script:

```
import sys
from pathlib import Path

# Add src/ to Python path
project_root = Path.cwd().parents[1]
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and use the display function
from ai_misko_asistentas.util.data_display import show_data_table

# Display the table
show_data_table("plant_examples.csv")
```

This will:

- Locate your CSV file under `data/`  
- Read and validate its contents  
- Embed the images directly into the HTML  
- Display an inline table like this:

| Image | Latin name |
|--------|-------------|
| `<img src="data:image/jpeg;base64,...">` | rubus idaeus |
| `<img src="data:image/jpeg;base64,...">` | amanita muscaria |
| `<img src="data:image/jpeg;base64,...">` | cantharellus cibarius |
| `<img src="data:image/jpeg;base64,...">` | vaccinium myrtillus |

---

## Notes

- The function `csv_dir.resolve()` (called internally) ensures all file paths are converted to absolute paths before reading, so the display works regardless of where the script is executed.  
- If you change or move the `data` folder, ensure the path logic in `show_data_table()` still points to the correct directory.  
- To see debug output (like which CSV is being loaded), you can add temporary `print()` statements inside `show_data_table()`.
