import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import csv
import json

# Define the bbox_to_yolo function
def bbox_to_yolo(bbox, image_width, image_height):
    xmin, ymin, xmax, ymax = bbox
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    width = xmax - xmin
    height = ymax - ymin
    x = x_center / image_width
    y = y_center / image_height
    width /= image_width
    height /= image_height
    return x, y, width, height

def bbox_to_yolo_two(bbox, image_width, image_height):
    x_min, y_min, width, height = bbox
    x = (x_min * 0.01) + (width * 0.01 /2)
    y = (y_min * 0.01) + (height * 0.01 /2)
    width = width * 0.01
    height = height * 0.01
    return x, y, width, height
    
def format_bboxes_to_yolo(bboxes):
    formatted_bboxes = []
    for i, bbox in enumerate(bboxes, start=2):
        formatted_bbox = f"{2} {' '.join(str(coord) for coord in bbox)}"
        formatted_bboxes.append(formatted_bbox)
    return formatted_bboxes

def clean_column(cell):
    cell_str = str(cell)
    cell_str = cell_str.replace('[', '').replace(']', '')
    cell_str = cell_str.replace("'", "")
    cell_str = cell_str.replace(",", "\n")
    return cell_str

def clean_column_two(cell):
    cell_str = str(cell)
    cell_str = cell_str.replace('[[', '').replace(']]', '').replace(']', '')
    cell_str = cell_str.replace(",", "")
    cell_str = cell_str.replace("[", "\n")
    return cell_str

def concatenate_columns(row):
    return f" {row['formatted_yolo_bboxes']} \n {row['merged_boxes']}"  # Modify this based on your column names

# Function to parse JSON and extract values
def parse_json(row):
    try:
        json_data = json.loads(row)
        if json_data:  # Check if JSON data is not empty
            extracted_data_1 = []
            extracted_data_0 = []
            for data in json_data:
                labels = data["label"]
                label = 0 if any(label in labels for label in ["face"]) else 1
                values = [data["x"] * 0.01 + data["width"] * 0.01 / 2, data["y"] * 0.01 + data["height"] * 0.01 /2, data["width"] * 0.01 , data["height"] * 0.01]
                if label == 1:
                    extracted_data_1.append([label] + values)
                else:
                    extracted_data_0.append([label] + values)
            return extracted_data_1 + extracted_data_0
    except (json.JSONDecodeError, IndexError):
        pass
    # Return NaN for invalid or empty JSON data
    return [[float('nan')] * 5]


# Read the CSV file
df = pd.read_csv('output2.csv')

# Delete columns
columns_to_delete = ['created_at', 'total_boxes', 
                     'det_polygons', 'det_scores', 'id_x', 'id_y'
                    #  'annotations', 'drafts', 'predictions', 
                    #  'agreement', 'meta', 'created_at_y', 'updated_at',
                    #  'inner_id', 'total_annotations', 'cancelled_annotations',
                    #  'total_predictions', 'comment_count', 'unresolved_comment_count',
                    #  'last_comment_updated_at',	'project',	'updated_by', 'comment_authors',
                    #  'data','file_upload', 'id'
                     ]
df = df.drop(columns=columns_to_delete)

# Rename columns
column_mapping = {'ID': 'asset_id'}
df = df.rename(columns=column_mapping)


df['yolo_bboxes'] = df.apply(lambda row: [bbox_to_yolo(bbox, row['width'], row['height']) for bbox in eval(row['bbox'])], axis=1)
df.drop(columns=['bbox'], inplace=True)
df.to_csv('output.csv', index=False)

new_df = pd.read_csv('output.csv')
new_columns = new_df['merged_boxes'].apply(parse_json)
new_df = new_df.drop(columns = ['merged_boxes'])

# Combine the new columns with the original DataFrame
new_df = pd.concat([new_df, new_columns], axis=1)
new_df['merged_boxes'] = new_df['merged_boxes'].apply(clean_column_two)

new_df['formatted_yolo_bboxes'] = new_df['yolo_bboxes'].apply(lambda x: format_bboxes_to_yolo(eval(x)) if isinstance(x, str) else [])
new_df['formatted_yolo_bboxes'] = new_df['formatted_yolo_bboxes'].apply(clean_column)
new_df['labels'] = new_df.apply(concatenate_columns, axis=1)

# Drop the original column
new_df.to_csv('output.csv', index=False)

new_new_df = pd.read_csv('output.csv')
columns_to_delete_2 = ['formatted_yolo_bboxes', 'merged_boxes', 'yolo_bboxes']
new_new_df = new_new_df.drop(columns=columns_to_delete_2)
new_column_order = ['asset_id', 'width', 'height', 'uri', 'labels']
# Reorder DataFrame columns
new_new_df = new_new_df.reindex(columns=new_column_order)
# Replace the word "khar" with an empty string in all columns
new_new_df = new_new_df.replace('nan', '', regex=True)
new_new_df.to_csv('tiktok_flt_cleared_new.csv', index=False)
new_new_df.to_parquet('tiktok_flt_cleared_new.parquet', index=False)