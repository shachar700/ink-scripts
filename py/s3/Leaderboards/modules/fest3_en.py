# modules/fest3_en.py
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
    Process challenge JSON for Solo / Pair / Team leaderboards.
    Supports GUI (with input_path provided) and headless/auto_run.
    """
    # If no input_path provided, open file dialog (GUI mode)
    if not input_path:
        input_path = _ask_for_file()
        if not input_path:
            logger("No file selected.")
            return

    start_time = time.time()

    with open(input_path, 'r', encoding='utf8') as fh:
        data = json.load(fh)

    start_time = time.time()

    # find badgemap relative to this file
    this_dir = Path(__file__).resolve().parent
    data_dict_badges = _utils.load_badgemap(this_dir)

    out_path = _utils.ensure_output_path(input_path, output_dir)
    logger(f"Writing output to {out_path}")

    with open(out_path, "w", encoding="utf8") as out:
        if 'fest' in data['data']:
            for team in data['data']['fest']['teams']:
                out.write("==== " + team["teamName"] + " ====\n")
                out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
                out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")
                for player_edge in team['result']['rankingHolders']['edges']:
                    player = player_edge["node"]
                    rank = player.get("rank", "")
                    name = player.get("name", "")
                    nameid = player.get("nameId", "")
                    if "|" in name or "~" in name:
                        name = "<nowiki>" + name + "</nowiki>"
                    power = player.get("festPower", "")
                    weapon = player["weapon"]["name"]
                    title = player.get("byname", "")
                    banner = _utils.decode_base64_id(player["nameplate"]["background"]["id"], prefix_trim=20)
                    badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                    out.write("|-\n")
                    out.write("| " + str(rank) + " || " + str(power) + " || {{Splashtag|title=" + title +
                              "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                    if badgeslist != ['Null', 'Null', 'Null']:
                        if badgeslist[0] in data_dict_badges:
                            out.write("|badge1=" + data_dict_badges[badgeslist[0]])
                        if badgeslist[1] in data_dict_badges:
                            out.write("|badge2=" + data_dict_badges[badgeslist[1]])
                        if badgeslist[2] in data_dict_badges:
                            out.write("|badge3=" + data_dict_badges[badgeslist[2]])
                    out.write("}}\n" +
                              "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")
                out.write("|}\n\n")
        elif 'node' in data['data']:
            for player_edge in data['data']['node']['result']['rankingHolders']['edges']:
                player = player_edge["node"]
                rank = player.get("rank", "")
                name = player.get("name", "")
                nameid = player.get("nameId", "")
                if "|" in name or "~" in name:
                    name = "<nowiki>" + name + "</nowiki>"
                power = player.get("festPower", "")
                weapon = player["weapon"]["name"]
                title = player.get("byname", "")
                banner = _utils.decode_base64_id(player["nameplate"]["background"]["id"], prefix_trim=20)
                badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                out.write("|-\n")
                out.write("| " + str(rank) + " || " + str(power) + " || {{Splashtag|title=" + title +
                          "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                if badgeslist != ['Null', 'Null', 'Null']:
                    if badgeslist[0] in data_dict_badges:
                        out.write("|badge1=" + data_dict_badges[badgeslist[0]])
                    if badgeslist[1] in data_dict_badges:
                        out.write("|badge2=" + data_dict_badges[badgeslist[1]])
                    if badgeslist[2] in data_dict_badges:
                        out.write("|badge3=" + data_dict_badges[badgeslist[2]])
                out.write("}}\n" +
                          "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

    elapsed = time.time() - start_time
    logger(f"Done! took {elapsed:.3f} seconds")
