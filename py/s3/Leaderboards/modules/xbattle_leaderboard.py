import json
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import utils as _utils


def _ask_for_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])


def process(input_path=None, output_dir=None, logger=print):
    """
    Handles all X Rank leaderboard modes (Cl, Lf, Ar, Gl).
    Supports both splatnet3 and splatoon3.ink JSON formats.
    """
    if not input_path:
        input_path = _ask_for_file()
    if not input_path:
        logger("No file selected.")
        return

    start_time = time.time()

    with open(input_path, "r", encoding="utf8") as fh:
        data = json.load(fh)

    this_dir = Path(__file__).resolve().parent
    badgemap = _utils.load_badgemap(this_dir)

    # Normalize JSON structure
    if "xRanking" in data.get("data", {}):
        # splatnet3
        season_data = data["data"]["xRanking"]["currentSeason"]

        def get_edges(key):
            nodes = season_data.get(key, {}).get("nodes", [])
            return [{"node": n} for n in nodes]

    elif "node" in data.get("data", {}):
        # splatoon3.ink
        node_data = data["data"]["node"]

        def get_edges(key):
            return node_data.get(key, {}).get("edges", [])
    else:
        logger("Unknown JSON format")
        return

    # Mode map
    mode_map = {
        "xRankingCl": "Clam Blitz",
        "xRankingLf": "Tower Control",
        "xRankingAr": "Splat Zones",
        "xRankingGl": "Rainmaker",
    }

    for key, mode_name in mode_map.items():
        edges = get_edges(key)
        if not edges:
            continue

        # Build suffixed output path
        base_out_path = _utils.ensure_output_path(input_path, output_dir)
        out_path = str(
            Path(base_out_path).with_name(
                Path(base_out_path).stem + f"_{key}" + Path(base_out_path).suffix
            )
        )
        logger(f"Writing output to {out_path}")

        with open(out_path, "w", encoding="utf8") as out:
            out.write(f"==== X Rank Leaderboard ({mode_name}) ====\n")
            out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
            out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")

            for edge in edges:
                player = edge["node"]
                rank = player.get("rank", "")
                name = player.get("name", "")
                nameid = player.get("nameId", "")
                if "|" in name or "~" in name:
                    name = "<nowiki>" + name + "</nowiki>"
                power = player.get("xPower", "")
                weapon = player["weapon"]["name"]
                title = player.get("byname", "")
                banner = _utils.decode_base64_id(
                    player["nameplate"]["background"]["id"], prefix_trim=20
                )
                badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                out.write("|-\n")
                out.write(
                    f"| {rank} || {power} || {{Splashtag|title={title}|name={name}|banner={banner}|tagnumber={nameid}"
                )

                if badgeslist != ["Null", "Null", "Null"]:
                    if badgeslist[0] in badgemap:
                        out.write("|badge1=" + badgemap[badgeslist[0]])
                    if badgeslist[1] in badgemap:
                        out.write("|badge2=" + badgemap[badgeslist[1]])
                    if badgeslist[2] in badgemap:
                        out.write("|badge3=" + badgemap[badgeslist[2]])
                out.write("}}\n")
                out.write(
                    f"| [[File:S3 Weapon Main {weapon} 2D Current.png|24px|link={weapon}]] [[{weapon}]]\n"
                )

            out.write("|}\n\n")

    elapsed = time.time() - start_time
    logger(f"Done! took {elapsed:.3f} seconds")
