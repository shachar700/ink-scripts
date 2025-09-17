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
    Handles Best Nine Ranking leaderboard (BestNineRankingSeason).
    Outputs wiki table with all 9 weapons for each player.
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

    node = data.get("data", {}).get("node", {})
    if node.get("__typename") != "BestNineRankingSeason":
        logger("Unsupported JSON format: expected BestNineRankingSeason")
        return

    season_name = node.get("name", "Unknown Season")
    ranking_nodes = node.get("ranking", {}).get("nodes", [])

    # Build output path
    base_out_path = _utils.ensure_output_path(input_path, output_dir)
    out_path = str(
        Path(base_out_path).with_name(
            Path(base_out_path).stem + "_bestnine" + Path(base_out_path).suffix
        )
    )
    logger(f"Writing output to {out_path}")

    with open(out_path, "w", encoding="utf8") as out:
        out.write(f"==== Best Nine Leaderboard ({season_name}) ====\n")
        out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        out.write("! Rank !! Power Total !! Splashtag !! Best Nine Weapons\n")

        for player in ranking_nodes:
            rank = player.get("rank", "")
            name = player.get("name", "")
            nameid = player.get("nameId", "")
            if "|" in name or "~" in name:
                name = "<nowiki>" + name + "</nowiki>"
            title = player.get("byname", "")
            banner = _utils.decode_base64_id(
                player["nameplate"]["background"]["id"], prefix_trim=20
            )
            badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

            # Best Nine details
            best_nine = player.get("bestNine", {})
            power_total = best_nine.get("powerTotal", "")
            weapon_orders = best_nine.get("weaponPowerOrders9", {}).get("nodes", [])

            # Build weapon cell
            weapons_cell = []
            for weapon_entry in weapon_orders:
                weapon_name = weapon_entry.get("weapon", {}).get("name", "")
                weapon_power = weapon_entry.get("weaponPower", "")
                if weapon_name:
                    weapons_cell.append(
                        f"[[File:S3 Weapon Main {weapon_name} 2D Current.png|24px|link={weapon_name}]] "
                        f"{weapon_power}"
                    )

            if weapons_cell:
                weapons_text = "<div style=\"column-count:3; -moz-column-count:3; -webkit-column-count:3;\">"
                weapons_text += "<br>".join(weapons_cell)
                weapons_text += "</div>"
            else:
                weapons_text = ""

            # Write row
            out.write("|-\n")
            out.write(
                f"| {rank} || {power_total} || {{{{Splashtag|title={title}|name={name}|banner={banner}|tagnumber={nameid}"
            )
            if badgeslist != ["Null", "Null", "Null"]:
                if badgeslist[0] in badgemap:
                    out.write("|badge1=" + badgemap[badgeslist[0]])
                if badgeslist[1] in badgemap:
                    out.write("|badge2=" + badgemap[badgeslist[1]])
                if badgeslist[2] in badgemap:
                    out.write("|badge3=" + badgemap[badgeslist[2]])
            out.write("}}\n")
            out.write(f"| {weapons_text}\n")

        out.write("|}\n\n")

    elapsed = time.time() - start_time
    logger(f"Done! took {elapsed:.3f} seconds")
