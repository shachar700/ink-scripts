import base64
import json
import os
import re
import sys
import tkinter as tk
from subprocess import call
from tkinter import filedialog

import requests
from packaging import version

A_VERSION = "0.1.0"

def check_for_updates():
    '''Checks the script version against the repo, reminding users to update if available.'''

    try:
        latest_script = requests.get("https://raw.githubusercontent.com/shachar700/ink-scripts/main/py/s3/Leaderboards/Challenge/challenge_lists_splatnet3.py")
        new_version = re.search(r'A_VERSION = "([\d.]*)"', latest_script.text).group(1)
        update_available = version.parse(new_version) > version.parse(A_VERSION)
        if update_available:
            print(f"\nThere is a new version (v{new_version}) available.", end='')
            if os.path.isdir(".git"):
                update_now = input("\nWould you like to update now? [Y/n] ")
                if update_now == "" or update_now[0].lower() == "y":
                    FNULL = open(os.devnull, "w")
                    call(["git", "checkout", "."], stdout=FNULL, stderr=FNULL)
                    call(["git", "checkout", "master"], stdout=FNULL, stderr=FNULL)
                    call(["git", "pull"], stdout=FNULL, stderr=FNULL)
                    print(f"Successfully updated to v{new_version}. Please restart s3s.")
                    sys.exit(0)
                else:
                    print("Please update to the latest version by running " \
                        '`\033[91m' + "git pull" + '\033[0m' \
                        "` as soon as possible.\n")
            else: # no git directory
                print(" Visit the site below to update:\nhttps://github.com/shachar700/ink-scripts\n")
    except Exception as e: # if there's a problem connecting to github
        print('\033[3m' + "» Couldn't connect to GitHub. Please update the script manually via " \
            '`\033[91m' + "git pull" + '\033[0m' + "`." + '\033[0m' + "\n")
        # print('\033[3m' + "» While s3s is in beta, please update the script regularly via " \
        # 	'`\033[91m' + "git pull" + '\033[0m' + "`." + '\033[0m' + "\n")

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
            # Process the data as needed
    else:
        print("No file selected.")

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
    os.path.join(current_dir, 'util', 'HelpingLists')
    # Relative path to the badgemap.txt file
    badgemap_path = os.path.join(current_dir, '..', 'util', 'HelpingLists', 'badgemap.txt')

    data_dict = {}
    with open(badgemap_path, 'r') as mapping:
        for line in mapping:
            k, v = line.strip().split(':')
            data_dict[k.strip()] = v.strip()

    # 0 for solo
    # 1 for pair
    # 2 for team
    data_solo = data['data']['rankingPeriod']['teams'][0]['details']['nodes']
    data_pair = data['data']['rankingPeriod']['teams'][1]['details']['nodes']
    data_team = data['data']['rankingPeriod']['teams'][2]['details']['nodes'] if len(
        data['data']['rankingPeriod']['teams']) > 2 else None

    return output_path, data_dict, data_solo, data_pair, data_team


def parse_text(output_path, data_dict, data_solo, data_pair, data_team):
    # Write data to the output file
    with open(output_path, 'w', encoding="utf8") as file_out:

        file_out.write("=== Solo ===\n")

        file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

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
                badge1 = "empty"

            if badges[1] is not None:
                badge2 = badges[1]["id"]
                badge2_bytes = badge2.encode('ascii')
                badge2_bytes = base64.b64decode(badge2_bytes)
                badge2 = badge2_bytes.decode('ascii')
                badge2 = badge2[6:]
            else:
                badge2 = "empty"

            if badges[2] is not None:
                badge3 = badges[2]["id"]
                badge3_bytes = badge3.encode('ascii')
                badge3_bytes = base64.b64decode(badge3_bytes)
                badge3 = badge3_bytes.decode('ascii')
                badge3 = badge3[6:]
            else:
                badge3 = "empty"

            file_out.write("|-\n")
            file_out.write("| " + str(rank) + " || " + str(power) + " || " + name + " <small>#" + nameid + "</small> " +
                           " || [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon +
                           "]] [[" + weapon + "]] || " + title + " || {{UserSplashtag|" + banner)

            if badge1 in data_dict:
                file_out.write("|" + data_dict[badge1])
            if badge2 in data_dict:
                file_out.write("|" + data_dict[badge2])
            if badge3 in data_dict:
                file_out.write("|" + data_dict[badge3])

            file_out.write("}}\n")

        file_out.write("|}\n")

        file_out.write("=== Pair ===\n")

        file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

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
                    badge1 = "empty"

                if badges[1] is not None:
                    badge2 = badges[1]["id"]
                    badge2_bytes = badge2.encode('ascii')
                    badge2_bytes = base64.b64decode(badge2_bytes)
                    badge2 = badge2_bytes.decode('ascii')
                    badge2 = badge2[6:]
                else:
                    badge2 = "empty"

                if badges[2] is not None:
                    badge3 = badges[2]["id"]
                    badge3_bytes = badge3.encode('ascii')
                    badge3_bytes = base64.b64decode(badge3_bytes)
                    badge3 = badge3_bytes.decode('ascii')
                    badge3 = badge3[6:]
                else:
                    badge3 = "empty"

                file_out.write("| " + name + " <small>#" + nameid + "</small>" +
                               " || [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon +
                               "]] [[" + weapon + "]] || " + title + " || {{UserSplashtag|" + banner)

                if badge1 in data_dict:
                    file_out.write("|" + data_dict[badge1])
                if badge2 in data_dict:
                    file_out.write("|" + data_dict[badge2])
                if badge3 in data_dict:
                    file_out.write("|" + data_dict[badge3])

                file_out.write("}}\n")

                # Check if the player is not the last one in the list
                if idx < len(position["players"]) - 1:
                    file_out.write("|-\n")

        file_out.write("|}\n")

        if data_team:

            file_out.write("=== Team ===\n")

            file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
            file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

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
                    ""
                    ""
                    ""

                    if badges[0] is not None:
                        badge1 = badges[0]["id"]
                        badge1_bytes = badge1.encode('ascii')
                        badge1_bytes = base64.b64decode(badge1_bytes)
                        badge1 = badge1_bytes.decode('ascii')
                        badge1 = badge1[6:]
                    else:
                        badge1 = "empty"

                    if badges[1] is not None:
                        badge2 = badges[1]["id"]
                        badge2_bytes = badge2.encode('ascii')
                        badge2_bytes = base64.b64decode(badge2_bytes)
                        badge2 = badge2_bytes.decode('ascii')
                        badge2 = badge2[6:]
                    else:
                        badge2 = "empty"

                    if badges[2] is not None:
                        badge3 = badges[2]["id"]
                        badge3_bytes = badge3.encode('ascii')
                        badge3_bytes = base64.b64decode(badge3_bytes)
                        badge3 = badge3_bytes.decode('ascii')
                        badge3 = badge3[6:]
                    else:
                        badge3 = "empty"

                    file_out.write("| " + name + " <small>#" + nameid + "</small>" +
                                   " || [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon +
                                   "]] [[" + weapon + "]] || " + title + " || {{UserSplashtag|" + banner)

                    if badge1 in data_dict:
                        file_out.write("|" + data_dict[badge1])
                    if badge2 in data_dict:
                        file_out.write("|" + data_dict[badge2])
                    if badge3 in data_dict:
                        file_out.write("|" + data_dict[badge3])

                    file_out.write("}}\n")

                    # Check if the player is not the last one in the list
                    if idx < len(position["players"]) - 1:
                        file_out.write("|-\n")

            file_out.write("|}\n")

    print("Done!")

def main():
    """Main process, including setup."""
    check_for_updates()
    output_path, data_dict, data_solo, data_pair, data_team = get_data()
    if output_path and data_dict and data_solo and data_pair:
        parse_text(output_path, data_dict, data_solo, data_pair, data_team)

if __name__ == "__main__":
    main()
