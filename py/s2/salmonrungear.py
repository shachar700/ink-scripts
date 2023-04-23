import json

with open('C:/Users/User/Desktop/3.json') as f:
    data = json.load(f)

print(json.dumps(data, indent=4, sort_keys=True))

gear = data[0]["reward_gear"]["name"]
kind = data[0]["reward_gear"]["kind"]

if str(kind) == "clothes":
    kind = "Clothing"
print(gear)
print(kind)