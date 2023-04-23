import json

with open('C:/Users/User/Desktop/5.json') as f:
    data = json.load(f)

print(json.dumps(data, indent=4, sort_keys=True))