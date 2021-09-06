import json

with open('C:/Users/User/Desktop/bravojp.json', encoding="utf8") as f:
    data = json.load(f)

#print(json.dumps(data, indent=4, sort_keys=True))

#print("=== Europe ===")
#print("==== Treat ====")
print("{| class=\"wikitable sitecolor-s2 mw-collapsible mw-collapsed")
print("! Rank !! Name !! Splatfest Power !! Weapon !! Headgear !! Shoes")

for player in data:
    rank = player["order"]
    name = player["info"]["nickname"]
    if name.find("|") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    if name.find("~") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    power = player["score"]
    weapon = player["info"]["weapon"]["name"]
    if str(weapon) == "Zink Mini Splatling ":
        weapon = "Zink Mini Splatling"
    headgear = player["info"]["head"]["name"]
    shoes  = player["info"]["shoes"]["name"]
    print("|-")
    print("| " +   str(rank) + " || " + name + " || " + str(power)  + " || [[File:S2 Weapon Main " +weapon + ".png|24px|link=" +weapon + "]] [[" + weapon+ "]] || [[File:S2 Gear Headgear " + headgear + ".png|24px|link=" + headgear+"]] [[" + headgear + "]] ||" + "[[File:S2 Gear Shoes " +shoes + ".png|24px|link=" +shoes + "]] [[" + shoes+ "]]")

print("|}")