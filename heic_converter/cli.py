import argparse
from pathlib import Path
from heic_converter.convert import convert_heic_to

def run_cli():
    parser = argparse.ArgumentParser(description="Batch convert HEIC images to PNG, JPG, or WebP.")
    parser.add_argument("indir", help="Input folder with HEIC files")
    parser.add_argument("-o", "--outdir", help="Output folder", default=None)
    parser.add_argument("-f", "--format", help="Output format", choices=["png", "jpg", "webp"], default="png")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="List files that would be converted without processing")

    args = parser.parse_args()
    indir = Path(args.indir).resolve()
    outdir = Path(args.outdir).resolve() if args.outdir else indir / "converted"

    files = list(indir.glob("*.heic")) + list(indir.glob("*.HEIC"))
    if not files:
        print(f"No HEIC files found in {indir}")
        return

    for file in files:
        if args.dry_run:
            print(f"Would convert: {file.name}")
        else:
            success, msg = convert_heic_to(file, outdir, args.format, args.overwrite)
            print(msg)
