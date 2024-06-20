import csv
import ast
from collections import defaultdict

def merge_bboxes(bbox_list):
    # This function merges multiple bbox lists into a single list,
    # wrapping each bbox with square brackets
    merged_bboxes = []
    for bbox in bbox_list:
        merged_bboxes.append(f"[{', '.join(map(str, bbox))}]")
    return merged_bboxes

def extract_and_merge_id_bbox(input_csv, output_csv):
    id_bbox_dict = defaultdict(list)

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        csvreader = csv.reader(infile)
        
        # Skip the header of the input CSV file
        next(csvreader)

        for row in csvreader:
            if len(row) > 3 and row[3]:
                try:
                    # Convert the string representation of the dictionary to an actual dictionary
                    ann_dict = ast.literal_eval(row[3])
                    
                    # Extract 'image_id' and 'bbox' fields
                    image_id = ann_dict['image_id']
                    bbox = ann_dict['bbox']
                    
                    # Append bbox to the list of bboxes for this image_id
                    id_bbox_dict[image_id].append(bbox)
                except (ValueError, SyntaxError):
                    # Handle the case where the string cannot be parsed into a dictionary
                    print(f"Error parsing row: {row}")

    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        csvwriter = csv.writer(outfile)
        
        # Write the header for the output CSV file
        csvwriter.writerow(['image_id', 'bbox'])

        # Write the merged image_id and bboxes to the output CSV file
        for image_id, bboxes in id_bbox_dict.items():
            merged_bbox = merge_bboxes(bboxes)
            csvwriter.writerow([image_id, ', '.join(merged_bbox)])

# Example usage
input_csv = 'coco_raw_paulo.csv'  # Replace with the path to your input CSV file
output_csv = 'coco_output_paulo.csv'  # Replace with the path to your output CSV file

extract_and_merge_id_bbox(input_csv, output_csv)


# import json

# # Path to your input JSON file
# input_json_file = 'annotations.json'

# # Path to your output JSON file
# output_json_file = 'restructured_data.json'

# # Load the input JSON file
# with open(input_json_file, 'r') as f:
#     data = json.load(f)

# # Create a new dictionary to store restructured data
# restructured_data = {}

# # Iterate through the original data
# for key, value in data.items():
#     # image_id = value['image_id']
#     image_id =value['id']
#     if image_id not in restructured_data:
#         restructured_data[image_id] = []
#     restructured_data[image_id].append(value)

# # Write the restructured data to a new JSON file
# with open(output_json_file, 'w') as f:
#     json.dump(restructured_data, f, indent=4)

# print(f"Data restructured and saved to '{output_json_file}'")
