import sys
from heic_converter.cli import run_cli
from heic_converter.gui import run_gui

if __name__ == "__main__":
    if "--gui" in sys.argv:
        run_gui()
    else:
        run_cli()
