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

# Central version and update URL
current_s3splatop_version = "0.1.11"
current_splatoon3_version = "11.2.0"
update_url = "https://raw.githubusercontent.com/shachar700/ink-scripts/refs/heads/main/py/s3/Leaderboards/main.py"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"S3 SplaTop {current_s3splatop_version}")
        self.iconbitmap("favicon.ico")
        self.resizable(False, False)

        # Selected module and file
        self.selected_module_key = tk.StringVar(value=list(MODULES.keys())[0])
        self.input_path = tk.StringVar(value="")
        self.output_dir = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.output_name = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Module:").grid(row=0, column=0, sticky="w")
        module_combo = ttk.Combobox(frm, values=list(MODULES.keys()), textvariable=self.selected_module_key, state="readonly", width=28)
        module_combo.grid(row=0, column=1, sticky="ew", padx=(6,0))

        file_frame = ttk.Frame(frm, padding=8, relief="solid")
        file_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10,0))
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="Input JSON:").grid(row=0, column=0, sticky="w")
        ttk.Entry(file_frame, textvariable=self.input_path, width=36).grid(row=0, column=1, sticky="w", padx=(6,4))
        ttk.Button(file_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, sticky="w", padx=(0,0))

        ttk.Label(file_frame, text="Output directory:").grid(row=1, column=0, sticky="w", pady=(8,0))
        ttk.Entry(file_frame, textvariable=self.output_dir, width=36).grid(row=1, column=1, sticky="w", padx=(6,4), pady=(8,0))
        ttk.Button(file_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, sticky="w", padx=(0,0), pady=(8,0))

        ttk.Label(file_frame, text="Output file name:").grid(row=2, column=0, sticky="w", pady=(8,0))
        ttk.Entry(file_frame, textvariable=self.output_name, width=36).grid(row=2, column=1, sticky="w", padx=(6,4), pady=(8,0))

        ttk.Button(file_frame, text="Download", command=self.on_process).grid(row=2, column=2, sticky="w", padx=(0,0), pady=(8,0))

        self.notebook = ttk.Notebook(frm)
        self.notebook.grid(row=2, column=0, columnspan=3, pady=(10,0), sticky="nsw")

        self.log_tab = ttk.Frame(self.notebook)
        self.log_scroll_container = ttk.Frame(self.log_tab)
        self.log_scroll_container.pack(fill="both", expand=True, padx=4, pady=4)
        self.log_text = tk.Text(self.log_scroll_container, height=10, width=50, state="disabled", wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)
        self.notebook.add(self.log_tab, text="Logs")

        self.raw_tab = ttk.Frame(self.notebook)
        self.raw_scroll_container = ttk.Frame(self.raw_tab)
        self.raw_scroll_container.pack(fill="both", expand=True, padx=4, pady=4)
        self.raw_output_text = tk.Text(self.raw_scroll_container, height=10, width=50, state="disabled", wrap="word")
        self.raw_output_text.pack(side="left", fill="both", expand=True)
        self.notebook.add(self.raw_tab, text="Raw Output")

        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(2, weight=1)

        self._set_text(self.log_text, "")
        self._set_text(self.raw_output_text, "")

        self.update_idletasks()
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")

    def _default_output_name(self, input_path):
        return f"{Path(input_path).stem}_out.txt"

    def _sync_output_name_from_input(self, input_path):
        if not input_path:
            return None
        if not self.output_name.get().strip():
            default_name = self._default_output_name(input_path)
            self.output_name.set(default_name)
            return default_name
        return self.output_name.get().strip()

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.input_path.set(path)
            self._sync_output_name_from_input(path)
            self.log_msg(f"Selected input: {path}")
            self._update_output_tabs(output_path=self._current_output_path(path), input_path=path)

    def browse_output(self):
        path = filedialog.askdirectory(initialdir=self.output_dir.get())
        if path:
            self.output_dir.set(path)
            self.log_msg(f"Selected output directory: {path}")

    def _set_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.see("end")
        widget.configure(state="disabled")

    def _append_text(self, widget, text):
        widget.configure(state="normal")
        widget.insert("end", text + "\n")
        widget.see("end")
        widget.configure(state="disabled")

    def _current_output_path(self, input_path=None):
        if not input_path:
            input_path = self.input_path.get()
        output_name = self._sync_output_name_from_input(input_path)
        return _utils.ensure_output_path(input_path, self.output_dir.get(), output_name=output_name)

    def _update_output_tabs(self, output_path=None, input_path=None):
        if output_path and os.path.exists(output_path):
            with open(output_path, "r", encoding="utf8") as fh:
                content = fh.read()
            self._set_text(self.raw_output_text, content or "(empty output)")
            return

        if input_path and os.path.exists(input_path):
            with open(input_path, "r", encoding="utf8") as fh:
                content = fh.read()
            self._set_text(self.raw_output_text, content or "(empty input)")
            return

        self._set_text(self.raw_output_text, "No output file was generated yet.")

    def log_msg(self, text):
        self._append_text(self.log_text, text)

    def on_process(self):
        module_key = self.selected_module_key.get()
        module_path = MODULES[module_key]
        input_path = self.input_path.get()
        output_dir = self.output_dir.get()
        output_name = self._sync_output_name_from_input(input_path)

        if not input_path:
            # still use file dialog (you wanted dialogs)
            input_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if not input_path:
                messagebox.showwarning("No input", "No input file selected.")
                return
            self.input_path.set(input_path)
            self._sync_output_name_from_input(input_path)
            self.log_msg(f"Selected input: {input_path}")

        try:
            mod = import_module(module_path)
        except Exception as e:
            messagebox.showerror("Import error", f"Failed to import module {module_path}: {e}")
            return

        self.log_msg(f"Running module: {module_key}")
        try:
            # call module's process function. Provide logger function so module can log to GUI.
            mod.process(input_path, output_dir=output_dir, output_name=output_name, logger=self.log_msg)
            out_path = _utils.ensure_output_path(input_path, output_dir, output_name=output_name)
            self._update_output_tabs(output_path=out_path, input_path=input_path)
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
        _utils.check_for_updates(current_s3splatop_version, current_splatoon3_version, update_url, logger=print)
    except Exception as e:
        # keep it non-fatal for GUI
        print(f"Update check failed: {e}")

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
