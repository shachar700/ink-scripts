import json

with open('C:/Users/User/Desktop/Top500/splat_zones1.json') as f:
    data_sz1 = json.load(f)
data_sz = data_sz1["top_rankings"]
with open('C:/Users/User/Desktop/Top500/splat_zones2.json') as f:
    data_sz2 = json.load(f)
data_sz += data_sz2["top_rankings"]
with open('C:/Users/User/Desktop/Top500/splat_zones3.json') as f:
    data_sz3 = json.load(f)
data_sz += data_sz3["top_rankings"]
with open('C:/Users/User/Desktop/Top500/splat_zones4.json') as f:
    data_sz4 = json.load(f)
data_sz += data_sz4["top_rankings"]
with open('C:/Users/User/Desktop/Top500/splat_zones5.json') as f:
    data_sz5 = json.load(f)
data_sz += data_sz5["top_rankings"]

with open('C:/Users/User/Desktop/Top500/tower_control1.json') as f:
    data_tc1 = json.load(f)
data_tc = data_tc1["top_rankings"]
with open('C:/Users/User/Desktop/Top500/tower_control2.json') as f:
    data_tc2 = json.load(f)
data_tc += data_tc2["top_rankings"]
with open('C:/Users/User/Desktop/Top500/tower_control3.json') as f:
    data_tc3 = json.load(f)
data_tc += data_tc3["top_rankings"]
with open('C:/Users/User/Desktop/Top500/tower_control4.json') as f:
    data_tc4 = json.load(f)
data_tc += data_tc4["top_rankings"]
with open('C:/Users/User/Desktop/Top500/tower_control5.json') as f:
    data_tc5 = json.load(f)
data_tc += data_tc5["top_rankings"]

with open('C:/Users/User/Desktop/Top500/rainmaker1.json') as f:
    data_rm1 = json.load(f)
data_rm = data_rm1["top_rankings"]
with open('C:/Users/User/Desktop/Top500/rainmaker2.json') as f:
    data_rm2 = json.load(f)
data_rm += data_rm2["top_rankings"]
with open('C:/Users/User/Desktop/Top500/rainmaker3.json') as f:
    data_rm3 = json.load(f)
data_rm += data_rm3["top_rankings"]
with open('C:/Users/User/Desktop/Top500/rainmaker4.json') as f:
    data_rm4 = json.load(f)
data_rm += data_rm4["top_rankings"]
with open('C:/Users/User/Desktop/Top500/rainmaker5.json') as f:
    data_rm5 = json.load(f)
data_rm += data_rm5["top_rankings"]

with open('C:/Users/User/Desktop/Top500/clam_blitz1.json') as f:
    data_cb1 = json.load(f)
data_cb = data_cb1["top_rankings"]
with open('C:/Users/User/Desktop/Top500/clam_blitz2.json') as f:
    data_cb2 = json.load(f)
data_cb += data_cb2["top_rankings"]
with open('C:/Users/User/Desktop/Top500/clam_blitz3.json') as f:
    data_cb3 = json.load(f)
data_cb += data_cb3["top_rankings"]
with open('C:/Users/User/Desktop/Top500/clam_blitz4.json') as f:
    data_cb4 = json.load(f)
data_cb += data_cb4["top_rankings"]
with open('C:/Users/User/Desktop/Top500/clam_blitz5.json') as f:
    data_cb5 = json.load(f)
data_cb += data_cb5["top_rankings"]

#print(json.dumps(data_sz, indent=4, sort_keys=True))

#print("== Top 500 ==")

print("=== Splat Zones ===")
print("{| class=\"wikitable sitecolor-s2 mw-collapsible mw-collapsed")
print("! Change !! Rank !! Name !! X Power !! Weapon")

for player in data_sz:
    rank_change = player["rank_change"]
    if str(rank_change) == "None":
       rank_change = ""
    if str(rank_change) == "up":
            rank_change = "<center>{{color|▲|green}}</center>"
    if str(rank_change) == "down":
        rank_change = "<center>{{color|▼|red}}</center>"
    if str(rank_change) == "remain":
       rank_change = "<center>{{color|▶|grey}}</center>"
    rank = player["rank"]
    name = player["name"]
    if name.find("|") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    if name.find("~") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    weapon = player["weapon"]["name"]
    if str(weapon) == "Zink Mini Splatling ":
        weapon = "Zink Mini Splatling"
    power = player["x_power"]
    print("|-")
    print("| " + str(rank_change) + " || " + str(rank) + " || " + name + " || " + str(power)  + " || [[File:S2 Weapon Main " +weapon + ".png|24px|link=" +weapon + "]] [[" + weapon+ "]]")

print("|}")
print()
print("=== Tower Control ===")
print("{| class=\"wikitable sitecolor-s2 mw-collapsible mw-collapsed")
print("! Change !! Rank !! Name !! X Power !! Weapon")

for player in data_tc:
    rank_change = player["rank_change"]
    if str(rank_change) == "None":
       rank_change = ""
    if str(rank_change) == "up":
            rank_change = "<center>{{color|▲|green}}</center>"
    if str(rank_change) == "down":
        rank_change = "<center>{{color|▼|red}}</center>"
    if str(rank_change) == "remain":
       rank_change = "<center>{{color|▶|grey}}</center>"
    rank = player["rank"]
    name = player["name"]
    if name.find("|") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    if name.find("~") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    weapon = player["weapon"]["name"]
    if str(weapon) == "Zink Mini Splatling ":
        weapon = "Zink Mini Splatling"
    power = player["x_power"]
    print("|-")
    print("| " + str(rank_change) + " || " + str(rank) + " || " + name + " || " + str(power)  + " || [[File:S2 Weapon Main " +weapon + ".png|24px|link=" +weapon + "]] [[" + weapon+ "]]")

print("|}")
print()
print("=== Rainmaker ===")
print("{| class=\"wikitable sitecolor-s2 mw-collapsible mw-collapsed")
print("! Change !! Rank !! Name !! X Power !! Weapon")

for player in data_rm:
    rank_change = player["rank_change"]
    if str(rank_change) == "None":
       rank_change = ""
    if str(rank_change) == "up":
            rank_change = "<center>{{color|▲|green}}</center>"
    if str(rank_change) == "down":
        rank_change = "<center>{{color|▼|red}}</center>"
    if str(rank_change) == "remain":
       rank_change = "<center>{{color|▶|grey}}</center>"
    rank = player["rank"]
    name = player["name"]
    if name.find("|") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    if name.find("~") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    weapon = player["weapon"]["name"]
    if str(weapon) == "Zink Mini Splatling ":
        weapon = "Zink Mini Splatling"
    power = player["x_power"]
    print("|-")
    print("| " + str(rank_change) + " || " + str(rank) + " || " + name + " || " + str(power)  + " || [[File:S2 Weapon Main " +weapon + ".png|24px|link=" +weapon + "]] [[" + weapon+ "]]")

print("|}")
print()
print("=== Clam Blitz ===")
print("{| class=\"wikitable sitecolor-s2 mw-collapsible mw-collapsed")
print("! Change !! Rank !! Name !! X Power !! Weapon")

for player in data_cb:
    rank_change = player["rank_change"]
    if str(rank_change) == "None":
       rank_change = ""
    if str(rank_change) == "up":
            rank_change = "<center>{{color|▲|green}}</center>"
    if str(rank_change) == "down":
        rank_change = "<center>{{color|▼|red}}</center>"
    if str(rank_change) == "remain":
       rank_change = "<center>{{color|▶|grey}}</center>"
    rank = player["rank"]
    name = player["name"]
    if name.find("|") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    if name.find("~") > -1:
        name = "<nowiki>" + name + "</nowiki>"
    weapon = player["weapon"]["name"]
    if str(weapon) == "Zink Mini Splatling ":
        weapon = "Zink Mini Splatling"
    power = player["x_power"]
    print("|-")
    print("| " + str(rank_change) + " || " + str(rank) + " || " + name + " || " + str(power)  + " || [[File:S2 Weapon Main " +weapon + ".png|24px|link=" +weapon + "]] [[" + weapon+ "]]")

print("|}")
