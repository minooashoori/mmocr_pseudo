import json

with open('logodet3k_later_110000.json', 'r') as f:
    data = json.load(f)

# Delete the first n rows
del data[:2]

with open('logodet3k_later_110000.json', 'w') as f:
    json.dump(data, f, indent=4)