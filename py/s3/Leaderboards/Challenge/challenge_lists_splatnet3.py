import json
import time
import base64
import tkinter as tk
from tkinter import filedialog
import requests
import re
import os
import sys
from packaging import version
from subprocess import call

current_version = "0.1.4"
url = "https://raw.githubusercontent.com/shachar700/ink-scripts/refs/heads/main/py/s3/Leaderboards/Splatfest/fest3_for_splatoon3ink_3teams.py"

def check_for_updates():
    '''Checks the script version against the repo, reminding users to update if available.'''
    try:
        latest_script = requests.get(url)
        new_version = re.search(r'current_version = "([\d.]*)"', latest_script.text).group(1)
        print(f'Ink-scripts repo version: (local: v{current_version} / remote: v{new_version})')
        update_available = version.parse(new_version) > version.parse(current_version)

        if update_available:
            print(f"\nThere is a new version (v{new_version}) available.", end='')

            # Get the parent directory of the current script
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

            if os.path.isdir(os.path.join(parent_dir, ".git")):
                update_now = input("\nWould you like to update now? [y/n] ")
                if update_now == "" or update_now[0].lower() == "y":
                    FNULL = open(os.devnull, "w")
                    call(["git", "checkout", "."], stdout=FNULL, stderr=FNULL)
                    call(["git", "checkout", "master"], stdout=FNULL, stderr=FNULL)
                    call(["git", "pull"], stdout=FNULL, stderr=FNULL)
                    print(f"Successfully updated to v{new_version}. Please restart the script.")
                    sys.exit(0)
                else:
                    print("Please update to the latest version by running 'git pull' as soon as possible.\n")
                    sys.exit(0)
            else:
                print("Visit the site below to update:\nhttps://github.com/shachar700/ink-scripts\n")
    except Exception as e:
        print("» Couldn't connect to GitHub. Check if the version in update_checker.py matches the version in github.com/shachar700/ink-scripts/blob/main/py/s3/Leaderboards/util/update_checker.py`.\n")

def get_data():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select a file
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

    # Check if a file was selected
    if file_path:
        with open(file_path, 'r', encoding="utf8") as file_in:
            data = json.load(file_in)
            start_time = time.time()
            # Process the data as needed
    else:
        print("No file selected.")
        sys.exit(0)

    # Extract the base name of the input file (e.g., 'input_name' from 'input_name.json')
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the output file name by appending '_out' to the base name
    output_file_name = base_name + '_out' + '.txt'

    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Output file path
    output_path = os.path.join(home_dir, 'Downloads', output_file_name)

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Relative paths to the files
    os.path.join(current_dir, 'processed_data')
    # Relative path to the badgemap.txt file
    badgemap_path = os.path.join(current_dir, '..', 'processed_data', 'badgemap.txt')

    data_dict_badges = {}
    with open(badgemap_path, 'r') as mapping:
        for line in mapping:
            k, v = line.strip().split(':')
            data_dict_badges[k.strip()] = v.strip()

    # 0 for solo
    # 1 for pair
    # 2 for team
    data_solo = data['data']['rankingPeriod']['teams'][0]['details']['nodes']
    data_pair = data['data']['rankingPeriod']['teams'][1]['details']['nodes']
    data_team = data['data']['rankingPeriod']['teams'][2]['details']['nodes'] if len(
        data['data']['rankingPeriod']['teams']) > 2 else None

    return output_path, data_dict_badges, data_solo, data_pair, data_team, start_time


def parse_text(output_path, data_dict_badges, data_solo, data_pair, data_team, start_time):
    # Write data to the output file
    with open(output_path, 'w', encoding="utf8") as file_out:

        file_out.write("=== Solo ===\n")

        file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        file_out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")

        for player in data_solo:
            name = player["players"][0]['name']
            nameid = player["players"][0]["nameId"]
            rank = player['rank']
            if name.find("|") > -1:
                name = "<nowiki>" + name + "</nowiki>"
            if name.find("~") > -1:
                name = "<nowiki>" + name + "</nowiki>"
            power = player['power']
            weapon = player["players"][0]["weapon"]["name"]
            title = player["players"][0]["byname"]

            banner64 = player["players"][0]["nameplate"]["background"]["id"]
            banner64_bytes = banner64.encode('ascii')
            banner_bytes = base64.b64decode(banner64_bytes)
            banner = banner_bytes.decode('ascii')
            banner = banner[20:]
            badges = player["players"][0]["nameplate"]["badges"]

            if badges[0] is not None:
                badge1 = badges[0]["id"]
                badge1_bytes = badge1.encode('ascii')
                badge1_bytes = base64.b64decode(badge1_bytes)
                badge1 = badge1_bytes.decode('ascii')
                badge1 = badge1[6:]
            else:
                badge1 = "Null"

            if badges[1] is not None:
                badge2 = badges[1]["id"]
                badge2_bytes = badge2.encode('ascii')
                badge2_bytes = base64.b64decode(badge2_bytes)
                badge2 = badge2_bytes.decode('ascii')
                badge2 = badge2[6:]
            else:
                badge2 = "Null"

            if badges[2] is not None:
                badge3 = badges[2]["id"]
                badge3_bytes = badge3.encode('ascii')
                badge3_bytes = base64.b64decode(badge3_bytes)
                badge3 = badge3_bytes.decode('ascii')
                badge3 = badge3[6:]
            else:
                badge3 = "Null"
            badgeslist = [badge1, badge2, badge3]

            file_out.write("|-\n")
            file_out.write("| " + str(rank) + " || " + str(
                power) + " || {{Splashtag|title=" + title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

            if badgeslist != ['Null', 'Null', 'Null']:
                if badge1 in data_dict_badges:
                    file_out.write("|badge1=" + data_dict_badges[badge1])
                if badge2 in data_dict_badges:
                    file_out.write("|badge2=" + data_dict_badges[badge2])
                if badge3 in data_dict_badges:
                    file_out.write("|badge3=" + data_dict_badges[badge3])
            file_out.write("}}\n"
                           "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

        file_out.write("|}\n")

        file_out.write("=== Pair ===\n")

        file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        file_out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")

        for position in data_pair:

            rank = position['rank']
            power = position['power']
            file_out.write("|-\n")
            file_out.write("|rowspan=\"2\" | " + str(rank) + "\n")
            file_out.write("|rowspan=\"2\" | " + str(power) + "\n")

            for idx, player in enumerate(position["players"]):
                name = player['name']
                nameid = player["nameId"]

                if name.find("|") > -1:
                    name = "<nowiki>" + name + "</nowiki>"
                if name.find("~") > -1:
                    name = "<nowiki>" + name + "</nowiki>"
                weapon = player["weapon"]["name"]
                title = player["byname"]

                banner64 = player["nameplate"]["background"]["id"]
                banner64_bytes = banner64.encode('ascii')
                banner_bytes = base64.b64decode(banner64_bytes)
                banner = banner_bytes.decode('ascii')
                banner = banner[20:]
                badges = player["nameplate"]["badges"]

                if badges[0] is not None:
                    badge1 = badges[0]["id"]
                    badge1_bytes = badge1.encode('ascii')
                    badge1_bytes = base64.b64decode(badge1_bytes)
                    badge1 = badge1_bytes.decode('ascii')
                    badge1 = badge1[6:]
                else:
                    badge1 = "Null"

                if badges[1] is not None:
                    badge2 = badges[1]["id"]
                    badge2_bytes = badge2.encode('ascii')
                    badge2_bytes = base64.b64decode(badge2_bytes)
                    badge2 = badge2_bytes.decode('ascii')
                    badge2 = badge2[6:]
                else:
                    badge2 = "Null"

                if badges[2] is not None:
                    badge3 = badges[2]["id"]
                    badge3_bytes = badge3.encode('ascii')
                    badge3_bytes = base64.b64decode(badge3_bytes)
                    badge3 = badge3_bytes.decode('ascii')
                    badge3 = badge3[6:]
                else:
                    badge3 = "Null"
                badgeslist = [badge1, badge2, badge3]

                file_out.write("|| {{Splashtag|title=" + title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                if badgeslist != ['Null', 'Null', 'Null']:
                    if badge1 in data_dict_badges:
                        file_out.write("|badge1=" + data_dict_badges[badge1])
                    if badge2 in data_dict_badges:
                        file_out.write("|badge2=" + data_dict_badges[badge2])
                    if badge3 in data_dict_badges:
                        file_out.write("|badge3=" + data_dict_badges[badge3])
                file_out.write("}}\n"
                               "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

                # Check if the player is not the last one in the list
                if idx < len(position["players"]) - 1:
                    file_out.write("|-\n")

        file_out.write("|}\n")

        if data_team:

            file_out.write("=== Team ===\n")

            file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
            file_out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")

            for position in data_team:

                rank = position['rank']
                power = position['power']
                file_out.write("|-\n")
                # print("len position players: " + str(len(position["players"])))
                if len(position["players"]) == 3:
                    file_out.write("|rowspan=\"3\" | " + str(rank) + "\n")
                else:
                    file_out.write("|rowspan=\"4\" | " + str(rank) + "\n")
                if len(position["players"]) == 3:
                    file_out.write("|rowspan=\"3\" | " + str(power) + "\n")
                else:
                    file_out.write("|rowspan=\"4\" | " + str(power) + "\n")

                for idx, player in enumerate(position["players"]):
                    name = player['name']
                    nameid = player["nameId"]

                    if name.find("|") > -1:
                        name = "<nowiki>" + name + "</nowiki>"
                    if name.find("~") > -1:
                        name = "<nowiki>" + name + "</nowiki>"
                    weapon = player["weapon"]["name"]
                    title = player["byname"]

                    banner64 = player["nameplate"]["background"]["id"]
                    banner64_bytes = banner64.encode('ascii')
                    banner_bytes = base64.b64decode(banner64_bytes)
                    banner = banner_bytes.decode('ascii')
                    banner = banner[20:]
                    badges = player["nameplate"]["badges"]

                    if badges[0] is not None:
                        badge1 = badges[0]["id"]
                        badge1_bytes = badge1.encode('ascii')
                        badge1_bytes = base64.b64decode(badge1_bytes)
                        badge1 = badge1_bytes.decode('ascii')
                        badge1 = badge1[6:]
                    else:
                        badge1 = "Null"

                    if badges[1] is not None:
                        badge2 = badges[1]["id"]
                        badge2_bytes = badge2.encode('ascii')
                        badge2_bytes = base64.b64decode(badge2_bytes)
                        badge2 = badge2_bytes.decode('ascii')
                        badge2 = badge2[6:]
                    else:
                        badge2 = "Null"

                    if badges[2] is not None:
                        badge3 = badges[2]["id"]
                        badge3_bytes = badge3.encode('ascii')
                        badge3_bytes = base64.b64decode(badge3_bytes)
                        badge3 = badge3_bytes.decode('ascii')
                        badge3 = badge3[6:]
                    else:
                        badge3 = "Null"

                    file_out.write("|| {{Splashtag|title=" + title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                    if badgeslist != ['Null', 'Null', 'Null']:
                        if badge1 in data_dict_badges:
                            file_out.write("|badge1=" + data_dict_badges[badge1])
                        if badge2 in data_dict_badges:
                            file_out.write("|badge2=" + data_dict_badges[badge2])
                        if badge3 in data_dict_badges:
                            file_out.write("|badge3=" + data_dict_badges[badge3])
                    file_out.write("}}\n"
                                   "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

                    # Check if the player is not the last one in the list
                    if idx < len(position["players"]) - 1:
                        file_out.write("|-\n")

            file_out.write("|}\n")

    end_time = time.time()
    print(f'Done! took {end_time - start_time:.3f} seconds')

def main():
    """Main process, including setup."""
    check_for_updates()
    print(
        f'Disclaimer: This script works for data about Splatoon 3 v9.2.0, If your list is prior to 9.0.0 (August 30 2024) make sure to replace |banner=972 to'
        f' |banner=972 (revoked) for the championship banner.')
    output_path, data_dict, data_solo, data_pair, data_team, start_time = get_data()
    if output_path and data_dict and data_solo and data_pair:
        parse_text(output_path, data_dict, data_solo, data_pair, data_team, start_time)

if __name__ == "__main__":
    main()
