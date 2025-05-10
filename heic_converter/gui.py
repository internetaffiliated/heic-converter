import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from threading import Thread
import webbrowser
from heic_converter.convert import convert_heic_to

def run_gui():
    def browse():
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def start_conversion():
        folder_path = entry.get().strip()
        if not folder_path:
            messagebox.showerror("Input Required", "Please select a folder.")
            return

        folder = Path(folder_path).resolve()
        if not folder.is_dir():
            messagebox.showerror("Invalid Folder", f"{folder} is not a valid directory.")
            return

        convert_button.config(state=tk.DISABLED)
        open_button.config(state=tk.DISABLED)
        status_var.set("Converting...")
        summary_var.set("")
        progress["value"] = 0
        log.delete("1.0", tk.END)

        # Start background conversion
        Thread(target=convert_in_background, args=(folder,)).start()

    def convert_in_background(folder: Path):
        out_format = format_var.get().lower()
        outdir = folder / "converted"
        overwrite = overwrite_var.get()

        # Deduplicate HEIC files (case-insensitive)
        files = {f.resolve() for f in folder.glob("*") if f.suffix.lower() == ".heic"}
        files = sorted(files)
        total = len(files)
        success_count = 0

        if not files:
            status_var.set("No HEIC files found.")
            convert_button.config(state=tk.NORMAL)
            return

        for i, file in enumerate(files, start=1):
            success, msg = convert_heic_to(file, outdir, out_format, overwrite)
            if success:
                success_count += 1
            log.insert(tk.END, f"[{i}/{total}] {msg}\n")
            log.see(tk.END)
            status_var.set(f"Converting... ({i}/{total})")
            progress["value"] = int((i / total) * 100)

        status_var.set("✅ Conversion Complete")
        summary_var.set(f"{success_count}/{total} converted successfully")
        convert_button.config(state=tk.NORMAL)
        open_button.config(state=tk.NORMAL)

    def open_output_folder():
        folder_path = entry.get().strip()
        if not folder_path:
            return
        out_path = Path(folder_path).resolve() / "converted"
        if out_path.exists():
            webbrowser.open(out_path.as_uri())

    root = tk.Tk()
    root.title("HEIC Converter")
    root.geometry("520x480")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TCheckbutton", font=("Segoe UI", 10))

    ttk.Label(root, text="Input Folder:").pack(pady=(10, 2))
    entry = ttk.Entry(root, width=60)
    entry.pack(padx=10)
    ttk.Button(root, text="Browse", command=browse).pack(pady=2)

    ttk.Label(root, text="Output Format:").pack(pady=(10, 2))
    format_var = tk.StringVar(value="PNG")
    ttk.Combobox(root, textvariable=format_var, values=["PNG", "JPG", "WEBP"], state="readonly", width=10).pack()

    overwrite_var = tk.BooleanVar()
    ttk.Checkbutton(root, text="Overwrite Existing Files", variable=overwrite_var).pack(pady=5)

    convert_button = ttk.Button(root, text="Start Conversion", command=start_conversion)
    convert_button.pack(pady=10)

    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=(5, 0))

    status_var = tk.StringVar(value="Ready.")
    ttk.Label(root, textvariable=status_var).pack(pady=(5, 0))

    summary_var = tk.StringVar(value="")
    ttk.Label(root, textvariable=summary_var, foreground="gray").pack()

    open_button = ttk.Button(root, text="Open Output Folder", command=open_output_folder, state=tk.DISABLED)
    open_button.pack(pady=5)

    log = tk.Text(root, height=12, width=65, font=("Consolas", 9))
    log.pack(padx=10, pady=(10, 5))

    root.mainloop()
