# HEIC Converter 🖼️

A hybrid CLI + GUI tool to batch convert `.HEIC` images to PNG, JPG, or WebP. Built with Python.

## 🔧 Features

- CLI for power users
- Simple drag-and-drop GUI
- Supports PNG, JPG, WebP
- Overwrite toggle, dry run mode
- Logs output to terminal or GUI window

## 🚀 Install

```bash
git clone https://github.com/internetaffiliated/heic-converter.git
cd heic-converter
pip install -r requirements.txt
```

## 🖥️ Usage

### CLI

```bash
python heic-converter.py input_folder -f png  # default format: png
python heic-converter.py input_folder -f jpg --overwrite
python heic-converter.py input_folder --dry-run
```

### GUI

```bash
python heic-converter.py --gui
```

---

## License
MIT
