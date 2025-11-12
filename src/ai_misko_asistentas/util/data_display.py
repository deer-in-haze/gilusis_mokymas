from pathlib import Path
import base64, mimetypes
import pandas as pd
from IPython.display import HTML, display

def resolve_csv_path(data_dir: Path, csv_filename: str) -> Path:
    csv_path = (data_dir / csv_filename).resolve()
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    return csv_path

def ensure_required_columns(df: pd.DataFrame, required: set[str]) -> None:
    if not required.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns {sorted(required)}; found {list(df.columns)}"
        )

def resolve_image_path(base_dir: Path, path_str: str) -> Path:
    rel = Path(str(path_str).lstrip("/"))
    return (base_dir / rel).resolve()

def image_to_data_uri(img_path: Path) -> str:
    mime, _ = mimetypes.guess_type(img_path.name)
    if mime is None:
        mime = "image/jpeg"
    data = img_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

def to_img_tag(img_path: Path, width: int = 120) -> str:
    if not img_path.exists():
        return f'<span style="color:#b00;">Missing: {img_path.name}</span>'
    data_uri = image_to_data_uri(img_path)
    return f'<img src="{data_uri}" width="{width}" style="border-radius:10px;" alt="{img_path.name}">'

def list_missing_images(df: pd.DataFrame, base_dir: Path) -> list[str]:
    missing: list[str] = []
    for p in df["IMAGE_PATH"]:
        if not resolve_image_path(base_dir, p).exists():
            missing.append(str(p))
    return missing

def dataframe_with_inline_images(df: pd.DataFrame, base_dir: Path, img_width: int = 120) -> pd.DataFrame:
    img_html = df["IMAGE_PATH"].apply(
        lambda p: to_img_tag(resolve_image_path(base_dir, p), width=img_width)
    )
    return pd.DataFrame({"Image": img_html, "Latin name": df["LATIN_NAME"]})

def render_html_table(df: pd.DataFrame) -> HTML:
    return HTML(df.to_html(escape=False, index=False))

def show_data_table(csv_filename: str):
    print(f"Loading CSV: {csv_filename}")
    # project_root = .../gilusis_mokymas  (data lives directly under this)
    project_root = Path(__file__).resolve().parents[3]
    data_dir = project_root / "data"
    print(f"Loading CSV: {data_dir}")

    csv_path = resolve_csv_path(data_dir, csv_filename)
    df = pd.read_csv(csv_path)
    ensure_required_columns(df, {"IMAGE_PATH", "LATIN_NAME"})

    base_dir = csv_path.parent.resolve()  # == data/

    missing = list_missing_images(df, base_dir)
    if missing:
        print("⚠️ missing image files:", ", ".join(missing))

    out_df = dataframe_with_inline_images(df, base_dir, img_width=120)
    html = render_html_table(out_df)
    display(html)