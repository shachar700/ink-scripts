# modules/challenge.py
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

    # data['data']['rankingPeriod']['teams'] -> 0 solo,1 pair,2 team
    ranking_period = data['data'].get('rankingPeriod', {})
    teams = ranking_period.get('teams', [])

    data_solo = teams[0]['details']['nodes'] if len(teams) > 0 else []
    data_pair = teams[1]['details']['nodes'] if len(teams) > 1 else []
    data_team = teams[2]['details']['nodes'] if len(teams) > 2 else None

    out_path = _utils.ensure_output_path(input_path, output_dir)
    logger(f"Writing output to {out_path}")

    with open(out_path, 'w', encoding="utf8") as out:
        # Solo
        out.write("=== Solo ===\n")
        out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")
        for player in data_solo:
            pl = player["players"][0]
            name = pl.get('name', '')
            nameid = pl.get('nameId', '')
            rank = player.get('rank', '')
            if "|" in name or "~" in name:
                name = "<nowiki>" + name + "</nowiki>"
            power = player.get('power', '')
            weapon = pl["weapon"]["name"]
            title = pl.get("byname", "")

            banner = _utils.decode_base64_id(pl["nameplate"]["background"]["id"], prefix_trim=20)
            badgeslist = _utils.safe_badges_list(pl["nameplate"]["badges"])

            out.write("|-\n")
            out.write("| " + str(rank) + " || " + str(power) + " || {{Splashtag|title=" + title + "|name=" + name +
                      "|banner=" + banner + "|tagnumber=" + nameid)
            if badgeslist != ['Null', 'Null', 'Null']:
                if badgeslist[0] in badgemap:
                    out.write("|badge1=" + badgemap[badgeslist[0]])
                if badgeslist[1] in badgemap:
                    out.write("|badge2=" + badgemap[badgeslist[1]])
                if badgeslist[2] in badgemap:
                    out.write("|badge3=" + badgemap[badgeslist[2]])
            out.write("}}\n" +
                      "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")
        out.write("|}\n")

        # Pair
        out.write("=== Pair ===\n")
        out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")
        for position in data_pair:
            rank = position.get('rank', '')
            power = position.get('power', '')
            out.write("|-\n")
            out.write("|rowspan=\"2\" | " + str(rank) + "\n")
            out.write("|rowspan=\"2\" | " + str(power) + "\n")

            for idx, player in enumerate(position["players"]):
                name = player.get('name', '')
                nameid = player.get('nameId', '')
                if "|" in name or "~" in name:
                    name = "<nowiki>" + name + "</nowiki>"
                weapon = player["weapon"]["name"]
                title = player.get("byname", "")

                banner = _utils.decode_base64_id(player["nameplate"]["background"]["id"], prefix_trim=20)
                badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                out.write("|| {{Splashtag|title=" + title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)
                if badgeslist != ['Null', 'Null', 'Null']:
                    if badgeslist[0] in badgemap:
                        out.write("|badge1=" + badgemap[badgeslist[0]])
                    if badgeslist[1] in badgemap:
                        out.write("|badge2=" + badgemap[badgeslist[1]])
                    if badgeslist[2] in badgemap:
                        out.write("|badge3=" + badgemap[badgeslist[2]])
                out.write("}}\n" +
                          "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

                if idx < len(position["players"]) - 1:
                    out.write("|-\n")
        out.write("|}\n")

        # Team (optional)
        if data_team:
            out.write("=== Team ===\n")
            out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
            out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")
            for position in data_team:
                rank = position.get('rank', '')
                power = position.get('power', '')
                out.write("|-\n")
                if len(position["players"]) == 3:
                    out.write("|rowspan=\"3\" | " + str(rank) + "\n")
                else:
                    out.write("|rowspan=\"4\" | " + str(rank) + "\n")
                if len(position["players"]) == 3:
                    out.write("|rowspan=\"3\" | " + str(power) + "\n")
                else:
                    out.write("|rowspan=\"4\" | " + str(power) + "\n")

                for idx, player in enumerate(position["players"]):
                    name = player.get('name', '')
                    nameid = player.get('nameId', '')
                    if "|" in name or "~" in name:
                        name = "<nowiki>" + name + "</nowiki>"
                    weapon = player["weapon"]["name"]
                    title = player.get("byname", "")

                    banner = _utils.decode_base64_id(player["nameplate"]["background"]["id"], prefix_trim=20)
                    badgeslist = _utils.safe_badges_list(player["nameplate"]["badges"])

                    out.write("|| {{Splashtag|title=" + title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)
                    if badgeslist != ['Null', 'Null', 'Null']:
                        if badgeslist[0] in badgemap:
                            out.write("|badge1=" + badgemap[badgeslist[0]])
                        if badgeslist[1] in badgemap:
                            out.write("|badge2=" + badgemap[badgeslist[1]])
                        if badgeslist[2] in badgemap:
                            out.write("|badge3=" + badgemap[badgeslist[2]])
                    out.write("}}\n" +
                              "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

                    if idx < len(position["players"]) - 1:
                        out.write("|-\n")
            out.write("|}\n")

    elapsed = time.time() - start_time
    logger(f"Done! took {elapsed:.3f} seconds")
