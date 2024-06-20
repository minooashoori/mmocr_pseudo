import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import csv

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
df = pd.read_csv('merged_data.csv')

# Delete columns
columns_to_delete = ['created_at', 'total_boxes', 
                     'det_polygons', 'det_scores', 'asset_id', 'uri_y',
                     'boxes', 'box_type', 'has_face', 'has_logo',
                     's3_uri' ,'mnt_uri' ,'dbfs_uri'
                     ]
df = df.drop(columns=columns_to_delete)

# Rename columns
column_mapping = {'ID': 'asset_id', 'uri_x': 'uri'}
df = df.rename(columns=column_mapping)


df['yolo_bboxes'] = df.apply(lambda row: [bbox_to_yolo(bbox, row['width'], row['height']) for bbox in eval(row['bbox'])], axis=1)
df.to_csv('output.csv', index=False)

new_df = pd.read_csv('output.csv')

new_df['formatted_yolo_bboxes'] = new_df['yolo_bboxes'].apply(lambda x: format_bboxes_to_yolo(eval(x)) if isinstance(x, str) else [])
new_df['formatted_yolo_bboxes'] = new_df['formatted_yolo_bboxes'].apply(clean_column)
new_df['labels'] = new_df.apply(concatenate_columns, axis=1)


new_df.to_csv('output.csv', index=False)
new_new_df = pd.read_csv('output.csv')
columns_to_delete_2 = ['formatted_yolo_bboxes', 'yolo_annotations', 'bbox', 'yolo_bboxes']
new_new_df = new_new_df.drop(columns=columns_to_delete_2)
new_column_order = ['asset_id', 'width', 'height', 'uri', 'labels']
# Reorder DataFrame columns
new_new_df = new_new_df.reindex(columns=new_column_order)
# Replace the word "khar" with an empty string in all columns
new_new_df = new_new_df.replace('nan', '', regex=True)
new_new_df.to_csv('logofusion02_flt_cleared.csv', index=False)
new_new_df.to_parquet('logofusion02_flt_cleared.parquet', index=False)