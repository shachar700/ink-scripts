import json
import base64

# This program reads a JSON file and writes the contents to a text file with wiki markup.

with open("C:/Users/User/Downloads/festivals.ranking.AP.JUEA-00010.json", 'r', encoding="utf8") as file_in:
    data = json.load(file_in)

#data = data['data']['fest']['teams'][2]['result']['rankingHolders']['edges'] #0,1,2 for alpha,bravo,charlie teams

data_dict = {}
with open('C:/Users/User/Documents/github repositories/ink-scripts/py/s3/badgemap.txt', 'r') as mapping:
    for line in mapping:
        k, v = line.strip().split(':')
        data_dict[k.strip()] = v.strip()

#print(data_dict)

#create txt file if there aren't any there
with open('C:/Users/User/Downloads/fest_output.txt', 'w', encoding="utf8") as file_out:

    for team in data['data']['fest']['teams']:
        file_out.write("==== " + team["teamName"] +" ====\n")
        file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
        file_out.write("! Rank !! Name !! Power !! Weapon !! Title !! <br>Splashtag\n")
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
            print(badges)

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

            badgeslist = [badge1,badge2,badge3]
            print("badgeslist:")
            print(badgeslist)
            #for item in badgeslist:
                #mapping.find(badge1)

            #switch all cases

            file_out.write("|-\n")
            file_out.write("| " +  str(rank) + " || " + name + " <small>#" + nameid + "</small> || " + str(power)  +
                        " || [[File:S3 Weapon Main " +weapon + " 2D Current.png|24px|link=" +weapon +
                        "]] [[" + weapon+ "]] || " + title + " || {{UserSplashtag|" + banner)
            if badgeslist == ['empty', 'empty', 'empty']:
                print("all are empty")
            else:
                if badge1 in data_dict:
                    file_out.write("|" + data_dict[badge1])
                if badge2 in data_dict:
                    file_out.write("|" + data_dict[badge2])
                if badge3 in data_dict:
                    file_out.write("|" + data_dict[badge3])
            # if badge1 != '':
            #     file_out.write("|" + badgeslist[0])
            # if badge2 != '':
            #     file_out.write("|" + badgeslist[1])
            # if badge3 != '':
            #     file_out.write("|" + badgeslist[2])
            file_out.write("}}\n")

        file_out.write("|}\n\n")