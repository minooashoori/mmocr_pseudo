import pandas as pd
import ast

# Define the bbox_to_yolo function
def bbox_to_yolo(bbox, image_width, image_height):
    x, y, width, height = bbox
    x_center = (x + width / 2) / image_width
    y_center = (y + height / 2) / image_height
    width /= image_width
    height /= image_height
    return [x_center, y_center, width, height]

def format_bboxes_to_yolo(bboxes):
    formatted_bboxes = []
    for i, bbox in enumerate(bboxes, start=2):
        formatted_bbox = f"{2} {' '.join(str(coord) for coord in bbox)}"
        formatted_bboxes.append(formatted_bbox)
    return formatted_bboxes

# Define the function to clean the column
def clean_column(cell):
    # Convert the list to a string
    cell_str = str(cell)
    # Remove '[' and ']'
    cell_str = cell_str.replace('[', '').replace(']', '')
    # Remove single quotes
    cell_str = cell_str.replace("'", "")
    # Replace commas with space
    cell_str = cell_str.replace(",", "\n")
    return cell_str

def concatenate_columns(row):
    return f" {row['formatted_yolo_bboxes']} \n {row['yolo_annotations']}"  # Modify this based on your column names


# Read the CSV file
df = pd.read_csv('output2.csv')

# Delete columns
columns_to_delete = ['image_id']
df = df.drop(columns=columns_to_delete)

# Rename columns
column_mapping = {'id': 'asset_id'}
df = df.rename(columns=column_mapping)

# Define the function to convert bboxes to YOLO format
def convert_to_yolo(row):
    bboxes_str = row['bboxes']
    if isinstance(bboxes_str, str) and not pd.isnull(bboxes_str):
        bboxes = ast.literal_eval(bboxes_str)  # Safely evaluate the string representation of the list
        return [bbox_to_yolo(bbox, row['width'], row['height']) for bbox in bboxes]
    else:
        return []
# Apply the conversion function
df['yolo_bboxes'] = df.apply(convert_to_yolo, axis=1)

# Save the DataFrame to a new CSV file
df.to_csv('output.csv', index=False)

new_df = pd.read_csv('output.csv')

new_df['formatted_yolo_bboxes'] = new_df['yolo_bboxes'].apply(lambda x: format_bboxes_to_yolo(eval(x)) if isinstance(x, str) else [])
new_df['formatted_yolo_bboxes'] = new_df['formatted_yolo_bboxes'].apply(clean_column)
# new_df['labels'] = new_df.apply(concatenate_columns, axis=1)


new_df.to_csv('output.csv', index=False)
new_new_df = pd.read_csv('output.csv')
columns_to_delete_2 = ['yolo_bboxes', 'bboxes']
new_new_df = new_new_df.drop(columns=columns_to_delete_2)
column_mapping = {'formatted_yolo_bboxes': 'labels'}
new_new_df = new_new_df.rename(columns=column_mapping)
# # new_column_order = ['asset_id', 'width', 'height', 'uri', 'labels']
# # Reorder DataFrame columns
# # new_new_df = new_new_df.reindex(columns=new_column_order)
# # Replace the word "khar" with an empty string in all columns
# new_new_df = new_new_df.replace('nan', '', regex=True)
new_new_df.to_csv('cocotext_cleared.csv', index=False)
new_new_df.to_parquet('cocotext_cleared.parquet', index=False)

# new_df['formatted_yolo_bboxes'] = new_df['yolo_bboxes'].apply(lambda x: format_bboxes_to_yolo(eval(x)) if isinstance(x, str) else [])
# new_df['formatted_yolo_bboxes'] = new_df['formatted_yolo_bboxes'].apply(clean_column)
# new_df['labels'] = new_df.apply(concatenate_columns, axis=1)


# new_df.to_csv('output.csv', index=False)
# new_new_df = pd.read_csv('output.csv')
# columns_to_delete_2 = ['formatted_yolo_bboxes', 'yolo_annotations', 'bbox', 'yolo_bboxes']
# new_new_df = new_new_df.drop(columns=columns_to_delete_2)
# new_column_order = ['asset_id', 'width', 'height', 'uri', 'labels']
# # Reorder DataFrame columns
# new_new_df = new_new_df.reindex(columns=new_column_order)
# new_new_df.to_csv('logodet3k_val_flt_cleared.csv', index=False)
# new_new_df.to_parquet('logodet3k_val_flt_cleared.parquet', index=False)
# --------------------------------------------------------------
# with open('/home/ubuntu/mmocr/reconstructed_cocotext.json', 'r') as file:
#     data = json.load(file)
# image_bboxes = {}

# for image_id, bboxes_list in data.items():
#     for bbox_entry in bboxes_list:
#         bbox = bbox_entry['bbox']
#         if image_id not in image_bboxes:
#             image_bboxes[image_id] = []
#         image_bboxes[image_id].append(bbox)

# # Step 2: Write to CSV
# with open('output.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     # Write header
#     csvwriter.writerow(['image_id', 'bboxes'])
#     # Write data
#     for image_id, bboxes in image_bboxes.items():
#         csvwriter.writerow([image_id, bboxes])
        
# -----------------------------------------------------------------
# import os
# import pandas as pd
# from PIL import Image

# # Path to the directory containing the images
# image_directory = '/home/ubuntu/train2014'

# # Initialize a list to store the image information
# image_info = []

# # Iterate over each file in the directory
# for filename in os.listdir(image_directory):
#     if filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
#         try:
#             # Full path to the image file
#             image_path = os.path.join(image_directory, filename)
            
#             # Open the image using PIL
#             with Image.open(image_path) as img:
#                 width, height = img.size

#             # Save image information
#             image_info.append({'id': filename, 'width': width, 'height': height})
#             print(f'Processed {filename}: width={width}, height={height}')
#         except Exception as e:
#             print(f'Error processing {filename}: {e}')

# # Convert the list of dictionaries to a DataFrame
# df = pd.DataFrame(image_info)

# # Save DataFrame to CSV
# csv_file_path = 'image_dimensions.csv'
# df.to_csv(csv_file_path, index=False)

