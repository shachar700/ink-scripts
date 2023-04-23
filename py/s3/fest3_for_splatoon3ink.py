import json
import base64

with open('C:/Users/User/Downloads/apfest.json', 'r', encoding="utf8") as file_in:
    data = json.load(file_in)

data = data['data']['fest']['teams'][2]['result']['rankingHolders']['edges'] #0,1,2 for alpha,bravo,charlie teams

data_dict = {}
with open('C:/Users/User/PycharmProjects/pythonProjectInkipedia/badgemap.txt', 'r') as mapping:
    for line in mapping:
        k, v = line.strip().split(':')
        data_dict[k.strip()] = v.strip()

#print(data_dict)

with open('C:/Users/User/Downloads/apfest_parsed.txt', 'w', encoding="utf8") as file_out:

    #print(data)

    #file_out.write("=== Europe ===")
    #file_out.write("==== Treat ====")
    file_out.write("{| class=\"wikitable sitecolor-s3 mw-collapsible mw-collapsed\n")
    file_out.write("! Rank !! Name !! Power !! Weapon !! Title !! <br>Splashtag\n")

    for player in data:
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
        badge1 = ''
        badge2 = ''
        badge3 = ''
        if badges != []:
            badge1 = badges[0]["id"]
            badge1_bytes = badge1.encode('ascii')
            badge1_bytes = base64.b64decode(badge1_bytes)
            badge1 = badge1_bytes.decode('ascii')
            badge1 = badge1[6:]
        if len(badges) > 1:
            badge2 = badges[1]["id"]
            badge2_bytes = badge2.encode('ascii')
            badge2_bytes = base64.b64decode(badge2_bytes)
            badge2 = badge2_bytes.decode('ascii')
            badge2 = badge2[6:]
        if len(badges) > 2:
            badge3 = badges[2]["id"]
            badge3_bytes = badge3.encode('ascii')
            badge3_bytes = base64.b64decode(badge3_bytes)
            badge3 = badge3_bytes.decode('ascii')
            badge3 = badge3[6:]
        badgeslist = [badge1,badge2,badge3]
        #for item in badgeslist:
            #mapping.find(badge1)

        #switch all cases

        file_out.write("|-\n")
        file_out.write("| " +  str(rank) + " || " + name + " <small>#" + nameid + "</small> || " + str(power)  +
                       " || [[File:S3 Weapon Main " +weapon + " Flat.png|24px|link=" +weapon +
                       "]] [[" + weapon+ "]] || " + title + " || {{UserSplashtag|" + banner)

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

    file_out.write("|}\n")