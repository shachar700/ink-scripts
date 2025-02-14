import os
import json
import sys
import time
import base64
import tkinter as tk
from tkinter import filedialog
from py.s3.Leaderboards.util.update_checker import check_for_updates

check_for_updates()
print(f'Disclaimer: This script works for data about Splatoon 3 v9.2.0, If your list is prior to 9.0.0 (August 30 2024) make sure to replace |banner=972 to'
      f' |banner=972 (revoked) for the championship banner.')

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
util_dir = os.path.join(current_dir, 'processed_data')
# Relative path to the badgemap.txt file
badgemap_path = os.path.join(current_dir, '..', 'processed_data', 'badgemap.txt')


data_dict_badges = {}
with open(badgemap_path, 'r') as mapping:
    for line in mapping:
        k, v = line.strip().split(':')
        data_dict_badges[k.strip()] = v.strip()


data = data['data']['node']['weaponTopsLf']

# Write data to the output file
with open(output_path, 'w', encoding="utf8") as file_out:
    file_out.write("==== Top Weapon Wielders ====\n")
    file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
    file_out.write("! Rank !! Power !! Splashtag !! <br>Weapon\n")
    #file_out.write("! Weapon !! Name !! Power !! Rank !! Title !! <br>Splashtag\n")

    last_category = None
    flag = False

    for edge in data['edges']:
        node = edge['node']

        # break when you finish 1 iteration
        if flag is True and node["weapon"]["name"] == "Sploosh-o-matic":
            break
        if node["weapon"]["name"] == "Sploosh-o-matic":
            flag = True

        # Check if 'weapon' exists and is not None
        if node.get('weapon') and node['weapon']['weaponCategory']['name']:
            weapon_category_name = node['weapon']['weaponCategory']['name']

            # Print the category only if it changes
            if weapon_category_name != last_category:
                file_out.write("|-\n")
                file_out.write("! colspan=\"4\" | " + weapon_category_name + "\n")
                last_category = weapon_category_name

        # For each player within this weapon category
        player = node
        rank = player["rank"]
        name = player["name"]
        nameid = player["nameId"]
        if name.find("|") > -1:
            name = "<nowiki>" + name + "</nowiki>"
        if name.find("~") > -1:
            name = "<nowiki>" + name + "</nowiki>"
        power = player["xPower"]
        weapon = player["weapon"]["name"]
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

    file_out.write("|}\n\n")

end_time = time.time()
print(f'Done! took {end_time-start_time:.3f} seconds')