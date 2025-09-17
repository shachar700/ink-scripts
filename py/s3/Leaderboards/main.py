# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pathlib import Path
from importlib import import_module
import utils as _utils

MODULES = {
    "(SplatNet3/Splatoon3.ink) Fest 3 (EN)": "modules.fest3_en",
    "(SplatNet3/Splatoon3.ink) Fest 3 (JP)": "modules.fest3_jp",
    "(SplatNet3) Challenges": "modules.challenge",
    "(SplatNet3/Splatoon3.ink) X Battle - Leaderboard": "modules.xbattle_leaderboard",
    "(SplatNet3/Splatoon3.ink) X Battle - Weapons": "modules.xbattle_weapons",
    "(SplatNet3) Best Nine": "modules.best_nine",
}

# Central version and update URL — check for updates only once (here)
current_version = "0.1.7"
update_url = "https://raw.githubusercontent.com/shachar700/ink-scripts/refs/heads/main/py/s3/LeaderboardsRefactored/main.py"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Splatoon3 Ink Scripts — GUI")
        self.geometry("640x360")
        self.resizable(False, False)

        # Selected module and file
        self.selected_module_key = tk.StringVar(value=list(MODULES.keys())[0])
        self.input_path = tk.StringVar(value="")
        self.output_dir = tk.StringVar(value=str(Path.home() / "Downloads"))

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Module:").grid(row=0, column=0, sticky="w")
        module_combo = ttk.Combobox(frm, values=list(MODULES.keys()), textvariable=self.selected_module_key, state="readonly")
        module_combo.grid(row=0, column=1, sticky="ew", columnspan=2, padx=(6,0))

        ttk.Label(frm, text="Input JSON:").grid(row=1, column=0, sticky="w", pady=(8,0))
        ttk.Entry(frm, textvariable=self.input_path, width=56).grid(row=1, column=1, sticky="w", pady=(8,0))
        ttk.Button(frm, text="Browse...", command=self.browse_input).grid(row=1, column=2, sticky="e", padx=(6,0), pady=(8,0))

        ttk.Label(frm, text="Output directory:").grid(row=2, column=0, sticky="w", pady=(8,0))
        ttk.Entry(frm, textvariable=self.output_dir, width=56).grid(row=2, column=1, sticky="w", pady=(8,0))
        ttk.Button(frm, text="Browse...", command=self.browse_output).grid(row=2, column=2, sticky="e", padx=(6,0), pady=(8,0))

        self.log = tk.Text(frm, height=12, width=78, state="disabled", wrap="word")
        self.log.grid(row=3, column=0, columnspan=3, pady=(12,0))

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(10,0))
        ttk.Button(btn_frame, text="Process", command=self.on_process).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Quit", command=self.destroy).grid(row=0, column=1, padx=6)

        frm.columnconfigure(1, weight=1)

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.input_path.set(path)
            self.log_msg(f"Selected input: {path}")

    def browse_output(self):
        path = filedialog.askdirectory(initialdir=self.output_dir.get())
        if path:
            self.output_dir.set(path)
            self.log_msg(f"Selected output directory: {path}")

    def log_msg(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def on_process(self):
        module_key = self.selected_module_key.get()
        module_path = MODULES[module_key]
        input_path = self.input_path.get()
        output_dir = self.output_dir.get()

        if not input_path:
            # still use file dialog (you wanted dialogs)
            input_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if not input_path:
                messagebox.showwarning("No input", "No input file selected.")
                return
            self.input_path.set(input_path)
            self.log_msg(f"Selected input: {input_path}")

        try:
            mod = import_module(module_path)
        except Exception as e:
            messagebox.showerror("Import error", f"Failed to import module {module_path}: {e}")
            return

        self.log_msg(f"Running module: {module_key}")
        try:
            # call module's process function. Provide logger function so module can log to GUI.
            mod.process(input_path, output_dir=output_dir, logger=self.log_msg)
            self.log_msg("Processing finished.")
            messagebox.showinfo("Done", "Processing finished. Check the output directory.")
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log_msg("Error during processing:\n" + str(e))
            messagebox.showerror("Processing error", f"An error occurred:\n{e}\n\nSee log for details.")
            print(tb)

def main():
    # check for updates once here
    try:
        _utils.check_for_updates(current_version, update_url, logger=print)
    except Exception as e:
        # keep it non-fatal for GUI
        print(f"Update check failed: {e}")

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
