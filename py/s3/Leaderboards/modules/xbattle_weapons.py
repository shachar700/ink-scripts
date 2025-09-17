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
    Handles all X Rank weapon top modes (Cl, Lf, Ar, Gl).
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
            nodes = season_data.get(key.replace("weaponTops", "xRanking"), {}).get("nodes", [])
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
        "weaponTopsCl": "Clam Blitz",
        "weaponTopsLf": "Tower Control",
        "weaponTopsAr": "Splat Zones",
        "weaponTopsGl": "Rainmaker",
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
            out.write(f"==== Top Weapon Wielders ({mode_name}) ====\n")
            out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
            out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")

            last_category = None
            flag = False

            for edge in edges:
                node = edge["node"]

                # keep original break-on-Sploosh logic
                if flag is True and node["weapon"]["name"] == "Sploosh-o-matic":
                    break
                if node["weapon"]["name"] == "Sploosh-o-matic":
                    flag = True

                # Category section header
                if (
                    node.get("weapon")
                    and node["weapon"].get("weaponCategory")
                    and node["weapon"]["weaponCategory"].get("name")
                ):
                    weapon_category_name = node["weapon"]["weaponCategory"]["name"]
                    if weapon_category_name != last_category:
                        out.write("|-\n")
                        out.write("! colspan=\"4\" | " + weapon_category_name + "\n")
                        last_category = weapon_category_name

                # Player row
                player = node
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
