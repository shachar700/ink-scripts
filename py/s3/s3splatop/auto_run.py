#!/usr/bin/env python3
import os
import sys
import importlib
import traceback
from pathlib import Path

def main():
    # --- Validate arguments ---
    if len(sys.argv) < 2:
        print("Usage: python auto_run.py <mode>")
        print("Example: python auto_run.py challenge")
        sys.exit(1)

    mode = sys.argv[1].lower()
    base_dir = Path(__file__).resolve().parent

    target_folder = base_dir / f"{mode}_top100"
    output_folder = base_dir / f"{mode}_top100_output"

    module_name = f"modules.{mode}"

    # --- Validate folder and module ---
    if not target_folder.is_dir():
        print(f"❌ Folder not found: {target_folder}")
        sys.exit(1)

    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        print(f"❌ Cannot import module: {module_name}")
        traceback.print_exc()
        sys.exit(1)

    # --- Check module entry point ---
    if not hasattr(module, "process"):
        print(f"❌ Module {module_name} has no function: process(path, output_dir)")
        sys.exit(1)

    print(f"🔍 Scanning: {target_folder}")
    print(f"📦 Using module: {module_name}")
    print(f"📁 Outputs will be saved in: {output_folder}")
    print("")

    # --- Walk the directory tree ---
    for root, dirs, files in os.walk(target_folder):
        root_path = Path(root)
        # Determine corresponding output subfolder
        relative_root = root_path.relative_to(target_folder)
        output_subfolder = output_folder / relative_root
        output_subfolder.mkdir(parents=True, exist_ok=True)

        print(f"📁 Folder: {root}")
        for file in files:
            if not file.endswith(".json"):
                continue

            input_path = root_path / file
            print(f"➡ Processing: {input_path}")

            try:
                # Pass the output subfolder to the module
                module.process(str(input_path), output_dir=str(output_subfolder))
            except Exception as e:
                print("❌ Error while processing:")
                traceback.print_exc()
            else:
                print(f"✔ Done: {file}")

        print("")

    print("🎉 All processing finished!")

if __name__ == "__main__":
    main()
