import os
import sys
import time
import json
import base64
import tkinter as tk
from tkinter import filedialog
from py.s3.Leaderboards.util.update_checker import check_for_updates

start_time = time.time()
check_for_updates()
print(f'Disclaimer: This script works for v9.2.0, If your list is prior to 9.0.0 make sure to replace |banner=972 to'
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
print(f'Done! took {end_time-start_time:.2f} seconds')