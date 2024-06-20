import json
from collections import defaultdict

# Path to your JSON file
input_json_file = 'cocotext.v2.json'

# Path to your output JSON file
output_json_file = 'annotations.json'

# Load the input JSON file
with open(input_json_file, 'r') as f:
    data = json.load(f)

# Access the 'annotations' part
annotations = data.get('anns', [])
# Get the keys (names of each part) of the top-level dictionary
part_names = list(data.keys())

# Print the part names
print("Names of each part in the JSON file:")
for part_name in part_names:
    print(part_name)
    
# Write the annotations to a new JSON file
with open(output_json_file, 'w') as f:
    json.dump(annotations, f, indent=4)

print(f"Annotations saved to '{output_json_file}'")