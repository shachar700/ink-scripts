# S3 SplaTop

 A small, user-friendly toolkit for processing Splatoon 3 JSON exports (SplatNet3 / Splatoon3.ink) and generating wiki markup outputs and leaderboards.

## Features
- Intuitive GUI for selecting processing modules and input JSON files.
- Batch runner for processing folders of JSON files.
- Multiple processing modules included: fest events, challenges, X Battle leaderboards, weapon summaries, and "best nine" extraction.
- Safe output path handling and simple update checks.

## Repository layout

- `main.py` — GUI application (Tkinter) to pick an input JSON, choose a module, and run processing.
- `auto_run.py` — CLI batch runner to process folders (useful for large runs / automation).
- `utils.py` — shared helper functions (output path handling, data loaders, update checker).
- `modules/` — processing modules (each exposes a `process(input_path, output_dir=..., output_name=..., logger=...)`).
- `preprocessed_data/` and `processed_data/` — supporting data files used by modules.

See also: [main.py](main.py), [auto_run.py](auto_run.py), [utils.py](utils.py)

## Requirements

- Python 3.8 or newer
- Dependencies (install via pip):

```bash
pip install requests packaging
```

Notes:
- `requests` is used by the built-in update checker in `utils.py`.
- `packaging` is used for version comparisons.

## Installation

1. Clone or download this repository.
2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows PowerShell
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt || pip install requests packaging
```

If you prefer, simply install `requests` and `packaging` directly as shown in Requirements.

## Quick Start — GUI

Run the GUI to load a single JSON and select a processor module:

```bash
python main.py
```

Usage notes:
- Choose a module from the dropdown, and select an input JSON.
- Optionally, select an output directory, an output file name, and click `Download`
- The GUI includes a Logs and Raw Output tab for quick inspection and a `Copy` button to copy raw output.

## Batch Processing — CLI

`auto_run.py` walks a folder named `<mode>_top` and outputs results to `<mode>_top_output` using the module at `modules.<mode>`.

Example:

```bash
# Process the 'challenge' mode (expects a folder named 'challenge_top')
python auto_run.py challenge
```

The script will import `modules.challenge` and call its `process()` for each JSON file in the folder tree.

## Modules

Each module in `modules/` should expose a `process(input_path, output_dir=None, output_name=None, logger=print)` function. The GUI passes a `logger` callback so modules can surface status messages in the GUI logs.

## Data files

The repository includes `preprocessed_data/` and `processed_data/` which modules may use to map weapon IDs, title text, and badge names. If a module expects these files, they are looked up relative to the calling module path (see `utils.load_badgemap` and `utils.load_titles`).

## Development

- To add a new processor, create `modules/<your_mode>.py` and implement `process()`.
- Keep outputs deterministic and respect `output_dir` when provided.

## Troubleshooting

- If the GUI fails to start on Windows, ensure `tkinter` is available for your Python installation.
- If the update check fails, it's non-fatal — network or repo layout may prevent remote parsing.

## License & Contact

S3 SplaTop is _free software_ licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html). This means that you have _freedom_ – to run, modify, copy, share, and redistribute this work as you see fit, as long as derivative works are also distributed under these same or equivalent terms.

While this is a free and open-source project, its license does require **attribution**. **If you are using any part of s3 splatop in your project, _please provide a link back to this repository_**.

For questions or contribution requests, open an issue or contact the maintainer.

---