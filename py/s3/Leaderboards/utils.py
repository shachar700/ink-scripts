# utils.py
import os
from pathlib import Path
import base64
import requests
import re
from packaging import version
from subprocess import call
import sys
import json

# Basic update checker — modules call this (keeps previous behavior)
def check_for_updates(current_version="0.1.0", url=None, logger=print):
    if not url:
        return
    try:
        logger("Checking for updates...")
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        m = re.search(r'current_version = "([\d.]*)"', resp.text)
        if not m:
            logger("Could not parse remote version.")
            return
        remote = m.group(1)
        logger(f"Local: v{current_version} / Remote: v{remote}")
        if version.parse(remote) > version.parse(current_version):
            logger(f"Update available: v{remote}")
            # If repo is a git clone (heuristic), prompt on console (keeps old behavior)
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            if os.path.isdir(os.path.join(parent_dir, ".git")):
                logger("Repository appears to be a git repo. Run 'git pull' to update.")
            else:
                logger("Visit https://github.com/shachar700/ink-scripts to update.")
    except Exception as e:
        logger(f"Couldn't check updates: {e}")

def home_downloads_path():
    return str(Path.home() / "Downloads")

def ensure_output_path(input_path, output_dir=None):
    base = os.path.splitext(os.path.basename(input_path))[0]
    fname = f"{base}_out.txt"
    if output_dir:
        return os.path.join(output_dir, fname)
    return os.path.join(home_downloads_path(), fname)

def load_badgemap(starting_path):
    # starting_path is usually modules folder; we look relative to that
    # Accept absolute path or build relative to project root
    p = Path(starting_path)
    candidate = p / "processed_data" / "badgemap.txt"
    if not candidate.exists():
        # second fallback: project root processed_data
        candidate = p.parent / "processed_data" / "badgemap.txt"
    data = {}
    if candidate.exists():
        with candidate.open("r", encoding="utf8") as fh:
            for line in fh:
                if ":" in line:
                    k, v = line.strip().split(":", 1)
                    data[k.strip()] = v.strip()
    return data

def load_titles(starting_path):
    p = Path(starting_path)
    adj = {}
    subj = {}
    a = p / "processed_data" / "titles_adj.txt"
    b = p / "processed_data" / "titles_sbj.txt"
    if not a.exists():
        a = p.parent / "processed_data" / "titles_adj.txt"
    if not b.exists():
        b = p.parent / "processed_data" / "titles_sbj.txt"
    if a.exists():
        with a.open("r", encoding="utf8") as fh:
            for line in fh:
                if ":" in line:
                    k, v = line.strip().split(":", 1)
                    adj[k.strip()] = v.strip()
    if b.exists():
        with b.open("r", encoding="utf8") as fh:
            for line in fh:
                if ":" in line:
                    k, v = line.strip().split(":", 1)
                    subj[k.strip()] = v.strip()
    return adj, subj

def decode_base64_id(b64string, prefix_trim=0):
    # these JSON fields are base64 of a string; decode and optionally trim prefix
    try:
        b = b64string.encode("ascii")
        decoded = base64.b64decode(b).decode("ascii")
        if prefix_trim:
            return decoded[prefix_trim:]
        return decoded
    except Exception:
        return b64string

def safe_badges_list(badges):
    # return normalized list of 3 entries
    out = []
    for i in range(3):
        try:
            if badges[i] is not None:
                s = badges[i]["id"]
                decoded = decode_base64_id(s, prefix_trim=6)
                out.append(decoded)
            else:
                out.append("Null")
        except Exception:
            out.append("Null")
    return out
