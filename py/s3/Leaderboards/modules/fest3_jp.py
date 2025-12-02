# modules/fest3_jp.py
import os
import time
import json
from pathlib import Path

import utils as _utils

def process(input_path=None, output_dir=None, logger=print):
    """
    Converted from challenge_lists_splatnet3.py
    Produces a wiki-formatted .txt output for Solo / Pair / Team leaderboards.
    """

    if not input_path:
        raise ValueError("process() requires 'input_path' when used headless.")

    start_time = time.time()

    with open(input_path, 'r', encoding="utf8") as fh:
        data = json.load(fh)

    this_dir = Path(__file__).resolve().parent
    badgemap = _utils.load_badgemap(this_dir)
    data_adj, data_subj = _utils.load_titles(this_dir)

    # load weapons mapping
    weapons_json_path = this_dir.parent / "preprocessed_data" / "weapon.json"
    data_weapons = []
    if weapons_json_path.exists():
        with open(weapons_json_path, 'r', encoding="utf8") as wfh:
            try:
                data_weapons = json.load(wfh)
            except Exception:
                logger("Failed to parse weapon.json; continuing without translations.")
    else:
        alt = this_dir.parent.parent / "preprocessed_data" / "weapon.json"
        if alt.exists():
            with open(alt, 'r', encoding="utf8") as wfh:
                try:
                    data_weapons = json.load(wfh)
                except Exception:
                    logger("Failed to parse weapon.json (alt); continuing without translations.")

    out_path = _utils.ensure_output_path(input_path, output_dir)
    logger(f"Writing output to {out_path}")

    with open(out_path, 'w', encoding="utf8") as out:
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

                    # translate weapon if matches Japanese name
                    if data_weapons:
                        for wn in data_weapons:
                            try:
                                if weapon in wn['name'].get('ja_JP', ''):
                                    weapon = wn['name'].get('en_US', weapon)
                                    break
                            except Exception:
                                continue

                    title = player.get("byname", "")
                    banner = _utils.decode_base64_id(player["nameplate"]["background"]["id"], prefix_trim=20)
                    badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                    adj_title = ""
                    subj_title = ""
                    for adjective in data_adj:
                        if adjective in title:
                            adj_title = data_adj[adjective]
                            break
                    for subject in data_subj:
                        if subject in title:
                            subj_title = data_subj[subject]
                            break

                    out.write("|-\n")
                    out.write("| " + str(rank) + " || " + str(power) + " || {{Splashtag|title=" + adj_title + " " + subj_title +
                              "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                    if badgeslist != ['Null', 'Null', 'Null']:
                        if badgeslist[0] in badgemap:
                            out.write("|badge1=" + badgemap[badgeslist[0]])
                        if badgeslist[1] in badgemap:
                            out.write("|badge2=" + badgemap[badgeslist[1]])
                        if badgeslist[2] in badgemap:
                            out.write("|badge3=" + badgemap[badgeslist[2]])
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

                # translate weapon if matches Japanese name
                if data_weapons:
                    for wn in data_weapons:
                        try:
                            if weapon in wn['name'].get('ja_JP', ''):
                                weapon = wn['name'].get('en_US', weapon)
                                break
                        except Exception:
                            continue

                title = player.get("byname", "")
                banner = _utils.decode_base64_id(player["nameplate"]["background"]["id"], prefix_trim=20)
                badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                adj_title = ""
                subj_title = ""
                for adjective in data_adj:
                    if adjective in title:
                        adj_title = data_adj[adjective]
                        break
                for subject in data_subj:
                    if subject in title:
                        subj_title = data_subj[subject]
                        break

                out.write("|-\n")
                out.write("| " + str(rank) + " || " + str(power) + " || {{Splashtag|title=" + adj_title + " " + subj_title +
                          "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                if badgeslist != ['Null', 'Null', 'Null']:
                    if badgeslist[0] in badgemap:
                        out.write("|badge1=" + badgemap[badgeslist[0]])
                    if badgeslist[1] in badgemap:
                        out.write("|badge2=" + badgemap[badgeslist[1]])
                    if badgeslist[2] in badgemap:
                        out.write("|badge3=" + badgemap[badgeslist[2]])
                out.write("}}\n" +
                          "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

    elapsed = time.time() - start_time
    logger(f"Done! took {elapsed:.3f} seconds")
