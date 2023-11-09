import json
import base64

with open('C:/Users/User/Downloads/new season 1st.json', 'r', encoding="utf8") as file_in:
    data = json.load(file_in)

# 0 for solo
# 1 for pair
# 2 for team
data_solo = data['data']['rankingPeriod']['teams'][0]['details']['nodes']
data_pair = data['data']['rankingPeriod']['teams'][1]['details']['nodes']
data_team = data['data']['rankingPeriod']['teams'][2]['details']['nodes']

data_dict = {}
with open('C:/Users/User/Documents/github repositories/ink-scripts/py/s3/badgemap.txt', 'r') as mapping:
    for line in mapping:
        k, v = line.strip().split(':')
        data_dict[k.strip()] = v.strip()

with open('C:/Users/User/Downloads/new_season_1st_parsed.txt', 'w', encoding="utf8") as file_out:

    file_out.write("===SOLO===\n")

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
                       " || [[File:S3 Weapon Main " + weapon + " Flat.png|24px|link=" + weapon +
                       "]] [[" + weapon + "]] || " + title + " || {{UserSplashtag|" + banner)

        if badge1 in data_dict:
            file_out.write("|" + data_dict[badge1])
        if badge2 in data_dict:
            file_out.write("|" + data_dict[badge2])
        if badge3 in data_dict:
            file_out.write("|" + data_dict[badge3])

        file_out.write("}}\n")

    file_out.write("|}\n")

    file_out.write("===PAIR===\n")

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
                           " || [[File:S3 Weapon Main " + weapon + " Flat.png|24px|link=" + weapon +
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

    file_out.write("===TEAM===\n")

    file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
    file_out.write("! Rank !! Power !! Name !! Weapon !! Title !! <br>Splashtag\n")

    for position in data_team:

        rank = position['rank']
        power = position['power']
        file_out.write("|-\n")
        print("len position players: " + str(len(position["players"])))
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
                           " || [[File:S3 Weapon Main " + weapon + " Flat.png|24px|link=" + weapon +
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
