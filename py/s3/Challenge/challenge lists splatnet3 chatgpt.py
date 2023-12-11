import json
import base64
from tkinter import filedialog
import os


def get_file_path(file_name):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, file_name)


def decode_base64(encoded_str):
    bytes_data = base64.b64decode(encoded_str.encode('ascii'))
    return bytes_data.decode('ascii')[20:]


def parse_badge(badge):
    if badge is not None:
        decoded_badge = decode_base64(badge["id"])
        return decoded_badge[6:]
    return "empty"


def write_player_data(file_out, player):
    if 'players' not in player:
        return  # Skip this player if 'players' key is not present

    players = player['players']

    for idx, player_info in enumerate(players):
        if 'name' not in player_info:
            continue  # Skip this player if 'name' key is not present

        name = player_info['name']
        nameid = player_info.get("nameId", "")
        name = "<nowiki>" + name + "</nowiki>" if "|" in name or "~" in name else name
        weapon = player_info.get("weapon", {}).get("name", "")
        title = player_info.get("byname", "")

        banner = decode_base64(player_info.get("nameplate", {}).get("background", {}).get("id", ""))
        badges = [parse_badge(b) for b in player_info.get("nameplate", {}).get("badges", [])]

        file_out.write(f"| {name} <small>#{nameid}</small>"
                       f" || [[File:S3 Weapon Main {weapon} Flat.png|24px|link={weapon}]] [[{weapon}]]"
                       f" || {title} || {{UserSplashtag|{banner}")

        for badge in badges:
            if badge in data_dict:
                file_out.write(f"|{data_dict[badge]}")

        file_out.write("}}\n")

        # Check if the player is not the last one in the list
        if idx < len(players) - 1:
            file_out.write("|-\n")


# Select JSON file using a dialog
file_path = filedialog.askopenfilename(title="Select JSON file", filetypes=[("JSON files", "*.json")])

with open(file_path, 'r', encoding="utf8") as file_in:
    data = json.load(file_in)

data_solo = data['data']['rankingPeriod']['teams'][0]['details']['nodes']
data_pair = data['data']['rankingPeriod']['teams'][1]['details']['nodes']
data_team = data['data']['rankingPeriod']['teams'][2]['details']['nodes']

data_dict = {}
with open(get_file_path('badgemap.txt'), 'r') as mapping:
    for line in mapping:
        k, v = line.strip().split(':')
        data_dict[k.strip()] = v.strip()

output_file_path = get_file_path('new_season_1st_parsed.txt')

with open(output_file_path, 'w', encoding="utf8") as file_out:
    # Write SOLO table
    file_out.write("===SOLO===\n")
    file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
    file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

    for idx, player in enumerate(data_solo):
        file_out.write("|-\n")
        if idx == 0:
            rowspan = len(data_solo)
            file_out.write(f"|rowspan=\"{rowspan}\" | {player['rank']}\n")
            file_out.write(f"|rowspan=\"{rowspan}\" | {player['power']}\n")

        write_player_data(file_out, player)

    file_out.write("|}\n")

    # Write PAIR table
    file_out.write("===PAIR===\n")
    file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
    file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

    for idx, position in enumerate(data_pair):
        file_out.write("|-\n")
        if idx == 0:
            rowspan = len(data_pair)
            file_out.write(f"|rowspan=\"{rowspan}\" | {position['rank']}\n")
            file_out.write(f"|rowspan=\"{rowspan}\" | {position['power']}\n")

        for player in position["players"]:
            write_player_data(file_out, player)

            if idx < len(data_pair) - 1:
                file_out.write("|-\n")

    file_out.write("|}\n")

    # Write TEAM table
    file_out.write("===TEAM===\n")
    file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
    file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

    for idx, position in enumerate(data_team):
        file_out.write("|-\n")
        if idx == 0:
            rowspan = len(data_team)
            file_out.write(f"|rowspan=\"{rowspan}\" | {position['rank']}\n")
            file_out.write(f"|rowspan=\"{rowspan}\" | {position['power']}\n")

        for player in position["players"]:
            write_player_data(file_out, player)

            if idx < len(data_team) - 1:
                file_out.write("|-\n")

    file_out.write("|}\n")
