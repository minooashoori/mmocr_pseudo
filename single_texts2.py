# import csv

# def save_bbox_data_from_csv(csv_file_path, output_dir):
#     with open(csv_file_path, 'r') as csv_file:
#         csv_reader = csv.reader(csv_file)
        
#         for row in csv_reader:
#             if len(row) != 2:
#                 print(f"Skipping improperly formatted row: {row}")
#                 continue
            
#             image_id = row[0]
#             bbox_data = row[1].replace("\\n", "\n")
            
#             output_file_path = f"{output_dir}/{image_id}.txt"
            
#             with open(output_file_path, 'w') as output_file:
#                 output_file.write(bbox_data)
#             print(f"Saved bbox data for image ID {image_id} to {output_file_path}")

# # Example usage
# csv_file_path = '/home/ubuntu/mmocr/cocotext_final_paulo.csv'  # Replace with your CSV file path
# output_dir = '/home/ubuntu/mmocr/output_folder_coco_2'   # Replace with your output directory

# save_bbox_data_from_csv(csv_file_path, output_dir)
import os

def convert_bbox_format(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()

    with open(output_file_path, 'w') as outfile:
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 5:
                try:
                    label = parts[0]
                    xmin = float(parts[1])
                    ymin = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    # Calculate xcenter and ycenter
                    xcenter = xmin + width / 2
                    ycenter = ymin + height / 2

                    # Write the converted values to the output file
                    outfile.write(f"{label} {xcenter} {ycenter} {width} {height}\n")
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")
            else:
                print(f"Skipping improperly formatted line: {line.strip()}")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)
            convert_bbox_format(input_file_path, output_file_path)
            print(f"Processed file: {input_file_path}")

# Example usage
input_dir = '/home/ubuntu/mmocr/output_folder_coco_2'  # Replace with the path to your input directory
output_dir = '/home/ubuntu/mmocr/output_folder_coco_3'  # Replace with the path to your output directory

process_directory(input_dir, output_dir)
