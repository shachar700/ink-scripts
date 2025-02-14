import os
import sys
import time
import json
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
        print("» Couldn't connect to GitHub. Check if the local version matches the remote version manually.\n")

check_for_updates()
print(f'Disclaimer: This script works for data about Splatoon 3 v9.2.0, If your list is prior to 9.0.0 (August 30 2024) make sure to replace |banner=972 to'
      f' |banner=972 (revoked) for the championship banner.')

#v9.2.0

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

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Relative paths to the files
util_dir = os.path.join(current_dir, 'processed_data')
# Relative path to the badgemap.txt file
badgemap_path = os.path.join(current_dir, '..', 'processed_data', 'badgemap.txt')

# Relative path to the weapon.json file
weapons_json_path = os.path.join(current_dir, '..', 'preprocessed_data', 'weapon.json')

# Relative path to the titles_adj.txt file
titles_adj_path = os.path.join(current_dir, '..', 'processed_data', 'titles_adj.txt')

# Relative path to the titles_sbj.txt file
titles_sbj_path = os.path.join(current_dir, '..', 'processed_data', 'titles_sbj.txt')


#data = data['data']['fest']['teams'][2]['result']['rankingHolders']['edges'] #0,1,2 for alpha,bravo,charlie teams

#extract mapping of badges from file to dictionary
data_dict_badges = {}
with open(badgemap_path, 'r') as mapping:
    for line in mapping:
        k, v = line.strip().split(':')
        data_dict_badges[k.strip()] = v.strip()

#Update weapons list from: https://stat.ink/api/v3/weapon
#extract weapon names from file to dictionary
with open(weapons_json_path, 'r', encoding="utf8") as weapons_json_file:
    data_weapons = json.load(weapons_json_file)

data_dict_adj = {}
with open(titles_adj_path, 'r', encoding="utf8") as titles_adj:
    for line in titles_adj:
        k, v = line.strip().split(':')
        data_dict_adj[k.strip()] = v.strip()

data_dict_subj = {}
with open(titles_sbj_path, 'r', encoding="utf8") as titles_subj:
    for line in titles_subj:
        k, v = line.strip().split(':')
        data_dict_subj[k.strip()] = v.strip()

#print(data_dict_adj)
#print(data_dict_subj)
#print(data_dict_titles)
#print(data_dict)

# Extract the base name of the input file (e.g., 'input_name' from 'input_name.json')
base_name = os.path.splitext(os.path.basename(file_path))[0]

# Create the output file name by appending '_out' to the base name
output_file_name = base_name + '_out' + '.txt'

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Output file path
output_path = os.path.join(home_dir, 'Downloads', output_file_name)

# Write data to the output file
with open(output_path, 'w', encoding="utf8") as file_out:
    if 'fest' in data['data']:  # Check if we have full data for teams
        for team in data['data']['fest']['teams']:
            file_out.write("==== " + team["teamName"] +" ====\n")
            file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
            file_out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")
            #in-case of pages 2-4 from splatnet3 app do the following:
            #comment the for team and the lines below it up to this point
            #replace the following for with this one: for player in data['data']['node']['result']['rankingHolders']['edges']:
            #remove indents with shift+tab or any other method your IDE/notepad uses
            for player in team['result']['rankingHolders']['edges']:
                player = player["node"]
                rank = player["rank"]
                name = player["name"]
                nameid = player["nameId"]
                if name.find("|") > -1:
                    name = "<nowiki>" + name + "</nowiki>"
                if name.find("~") > -1:
                    name = "<nowiki>" + name + "</nowiki>"
                power = player["festPower"]
                weapon = player["weapon"]["name"]

                for weapon_name in data_weapons:
                    if weapon in weapon_name['name']['ja_JP']:
                        weapon = weapon_name['name']['en_US']

                title = player["byname"]
                banner64 = player["nameplate"]["background"]["id"]
                banner64_bytes = banner64.encode('ascii')
                banner_bytes = base64.b64decode(banner64_bytes)
                banner = banner_bytes.decode('ascii')
                banner = banner[20:]
                badges = player["nameplate"]["badges"]
                badge1 = ""
                badge2 = ""
                badge3 = ""
                #print(badges)

                try:
                    if badges[0] is not None:
                        badge1 = badges[0]["id"]
                        badge1_bytes = badge1.encode('ascii')
                        badge1_bytes = base64.b64decode(badge1_bytes)
                        badge1 = badge1_bytes.decode('ascii')
                        badge1 = badge1[6:]
                    else:
                        badge1 = "Null"
                except IndexError:
                    print("Error: 'badges' list is too short, unable to access index 0. This is due to old pull from "
                          "SplatNet 3 before Ice Cream Splatfest where badge placements were not taken into account. "
                          "Make sure to re-pull the list from SplatNet 3 to take badge placements into account.")
                    sys.exit(1)

                try:
                    if badges[1] is not None:
                        badge2 = badges[1]["id"]
                        badge2_bytes = badge2.encode('ascii')
                        badge2_bytes = base64.b64decode(badge2_bytes)
                        badge2 = badge2_bytes.decode('ascii')
                        badge2 = badge2[6:]
                    else:
                        badge2 = "Null"
                except IndexError:
                    print("Error: 'badges' list is too short, unable to access index 1. This is due to old pull from "
                          "SplatNet 3 before Ice Cream Splatfest where badge placements were not taken into account. "
                          "Make sure to re-pull the list from SplatNet 3 to take badge placements into account.")
                    sys.exit(1)

                try:
                    if badges[2] is not None:
                        badge3 = badges[2]["id"]
                        badge3_bytes = badge3.encode('ascii')
                        badge3_bytes = base64.b64decode(badge3_bytes)
                        badge3 = badge3_bytes.decode('ascii')
                        badge3 = badge3[6:]
                    else:
                        badge3 = "Null"
                except IndexError:
                    print("Error: 'badges' list is too short, unable to access index 2. This is due to old pull from "
                          "SplatNet 3 before Ice Cream Splatfest where badge placements were not taken into account. "
                          "Make sure to re-pull the list from SplatNet 3 to take badge placements into account.")
                    sys.exit(1)
                badgeslist = [badge1, badge2, badge3]
                #for item in badgeslist:
                    #mapping.find(badge1)

                #print("title= " + title)

                # switch all cases
                for adjective in data_dict_adj:
                    if adjective in title:
                        adj_title = data_dict_adj[adjective]

                for subject in data_dict_subj:
                    if subject in title:
                        subj_title = data_dict_subj[subject]

                file_out.write("|-\n")
                file_out.write("| " + str(rank) + " || " + str(
                    power) + " || {{Splashtag|title=" + adj_title + " " + subj_title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

                if badgeslist != ['Null', 'Null', 'Null']:
                    if badge1 in data_dict_badges:
                        file_out.write("|badge1=" + data_dict_badges[badge1])
                    if badge2 in data_dict_badges:
                        file_out.write("|badge2=" + data_dict_badges[badge2])
                    if badge3 in data_dict_badges:
                        file_out.write("|badge3=" + data_dict_badges[badge3])
                file_out.write("}}\n"
                               "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

            file_out.write("|}\n\n")
    elif 'node' in data['data']:
        for player in data['data']['node']['result']['rankingHolders']['edges']:
            player = player["node"]
            rank = player["rank"]
            name = player["name"]
            nameid = player["nameId"]
            if name.find("|") > -1:
                name = "<nowiki>" + name + "</nowiki>"
            if name.find("~") > -1:
                name = "<nowiki>" + name + "</nowiki>"
            power = player["festPower"]
            weapon = player["weapon"]["name"]

            for weapon_name in data_weapons:
                if weapon in weapon_name['name']['ja_JP']:
                    weapon = weapon_name['name']['en_US']

            title = player["byname"]
            banner64 = player["nameplate"]["background"]["id"]
            banner64_bytes = banner64.encode('ascii')
            banner_bytes = base64.b64decode(banner64_bytes)
            banner = banner_bytes.decode('ascii')
            banner = banner[20:]
            badges = player["nameplate"]["badges"]
            badge1 = ""
            badge2 = ""
            badge3 = ""
            #print(badges)

            if badges[0] is not None:
                badge1 = badges[0]["id"]
                badge1_bytes = badge1.encode('ascii')
                badge1_bytes = base64.b64decode(badge1_bytes)
                badge1 = badge1_bytes.decode('ascii')
                badge1 = badge1[6:]
            else:
                badge1 = "Null"

            try:
                if badges[0] is not None:
                    badge1 = badges[0]["id"]
                    badge1_bytes = badge1.encode('ascii')
                    badge1_bytes = base64.b64decode(badge1_bytes)
                    badge1 = badge1_bytes.decode('ascii')
                    badge1 = badge1[6:]
                else:
                    badge1 = "Null"
            except IndexError:
                print("Error: 'badges' list is too short, unable to access index 0. This is due to old pull from "
                      "SplatNet 3 before Ice Cream Splatfest where badge placements were not taken into account. "
                      "Make sure to re-pull the list from SplatNet 3 to take badge placements into account.")
                sys.exit(1)

            try:
                if badges[1] is not None:
                    badge2 = badges[1]["id"]
                    badge2_bytes = badge2.encode('ascii')
                    badge2_bytes = base64.b64decode(badge2_bytes)
                    badge2 = badge2_bytes.decode('ascii')
                    badge2 = badge2[6:]
                else:
                    badge2 = "Null"
            except IndexError:
                print("Error: 'badges' list is too short, unable to access index 1. This is due to old pull from "
                      "SplatNet 3 before Ice Cream Splatfest where badge placements were not taken into account. Make "
                      "sure to re-pull the list from SplatNet 3 to take badge placements into account.")
                sys.exit(1)

            try:
                if badges[2] is not None:
                    badge3 = badges[2]["id"]
                    badge3_bytes = badge3.encode('ascii')
                    badge3_bytes = base64.b64decode(badge3_bytes)
                    badge3 = badge3_bytes.decode('ascii')
                    badge3 = badge3[6:]
                else:
                    badge3 = "Null"
            except IndexError:
                print("Error: 'badges' list is too short, unable to access index 2. This is due to old pull from "
                      "SplatNet 3 before Ice Cream Splatfest where badge placements were not taken into account. Make "
                      "sure to re-pull the list from SplatNet 3 to take badge placements into account.")
                sys.exit(1)
            badgeslist = [badge1, badge2, badge3]
            #for item in badgeslist:
                #mapping.find(badge1)

            #print("title= " + title)

            # switch all cases
            for adjective in data_dict_adj:
                if adjective in title:
                    adj_title = data_dict_adj[adjective]

            for subject in data_dict_subj:
                if subject in title:
                    subj_title = data_dict_subj[subject]

            file_out.write("|-\n")
            file_out.write("| " + str(rank) + " || " + str(
                power) + " || {{Splashtag|title=" + adj_title + " " + subj_title + "|name=" + name + "|banner=" + banner + "|tagnumber=" + nameid)

            if badgeslist != ['Null', 'Null', 'Null']:
                if badge1 in data_dict_badges:
                    file_out.write("|badge1=" + data_dict_badges[badge1])
                if badge2 in data_dict_badges:
                    file_out.write("|badge2=" + data_dict_badges[badge2])
                if badge3 in data_dict_badges:
                    file_out.write("|badge3=" + data_dict_badges[badge3])
            file_out.write("}}\n"
                           "| [[File:S3 Weapon Main " + weapon + " 2D Current.png|24px|link=" + weapon + "]] [[" + weapon + "]]\n")

        file_out.write("|}\n\n")

end_time = time.time()
print(f'Done! took {end_time-start_time:.3f} seconds')