import json

with open("wiretapping_config.json", "rb") as f:
    temp = json.load(f)

print(temp)