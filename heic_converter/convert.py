from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

def convert_heic_to(image_path: Path, out_dir: Path, out_format: str = "png", overwrite: bool = False) -> tuple[bool, str]:
    register_heif_opener()
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{image_path.stem}.{out_format.lower()}"
    if out_path.exists() and not overwrite:
        return False, f"Skipped: {out_path.name} already exists"

    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB") if out_format.lower() in ["jpg", "jpeg"] else img
            img.save(out_path, format=out_format.upper(), optimize=True)
        return True, f"✓ Converted: {image_path.name} → {out_path.name}"
    except Exception as e:
        return False, f"✗ Failed: {image_path.name} ({e})"
