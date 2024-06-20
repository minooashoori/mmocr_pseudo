import json

# Function to remove duplicate rows based on an ID column
def remove_duplicates(data, id_key):
    seen_ids = set()
    filtered_data = []
    num_removed = 0
    for item in data:
        if item[id_key] not in seen_ids:
            seen_ids.add(item[id_key])
            filtered_data.append(item)
        else:
            num_removed += 1
    return filtered_data, num_removed

# File paths of the JSON files
json_file1 = 'logofusion_mmocr.json'
json_file2 = 'logofusion_mmocr2.json'
output_file = 'logofusion_merged_file.json'

# Read data from the first JSON file
with open(json_file1, 'r') as f1:
    data1 = json.load(f1)

# Read data from the second JSON file
with open(json_file2, 'r') as f2:
    data2 = json.load(f2)

# Merge the data from both files
merged_data = data1 + data2

# Remove duplicate rows based on ID column
merged_data_filtered, num_removed = remove_duplicates(merged_data, 'ID')

# Write the filtered data to a new JSON file
with open(output_file, 'w') as output_f:
    json.dump(merged_data_filtered, output_f)

# Calculate the final number of rows
final_num_rows = len(merged_data_filtered)

print(f"Merged data from {json_file1} and {json_file2} into {output_file} after removing {num_removed} duplicates.")
print(f"Final number of rows: {final_num_rows}")
