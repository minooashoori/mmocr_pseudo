import os
import csv
import ast

def save_bbox_to_text(image_id, bbox_data, folder):
    try:
        # Convert the string representation of bbox_data into a list
        bbox_list = ast.literal_eval(bbox_data)
    except (SyntaxError, ValueError):
        print(f"Error parsing bbox_data for image_id {image_id}: {bbox_data}")
        return

    # Pad the image_id with leading zeros to make it 12 digits long
    padded_image_id = str(image_id).zfill(12)

    # Create the file name
    filename = f"COCO_train2014_{padded_image_id}.txt"
    file_path = os.path.join(folder, filename)

    with open(file_path, "w") as file:
        # Ensure bbox_list is a list of bounding boxes
        if isinstance(bbox_list, list) and len(bbox_list) == 4 and all(isinstance(i, (int, float)) for i in bbox_list):
            bbox_list = [bbox_list]  # Wrap in a list to process as a single bounding box
        
        for bbox in bbox_list:
            if isinstance(bbox, list) and len(bbox) == 4:
                bbox_rounded = [int(round(float(coord))) for coord in bbox]
                x, y, width, height = bbox_rounded
                x_center = x + width // 2
                y_center = y + height // 2
                bbox_str = f"2 {x_center} {y_center} {width} {height}"
                file.write(f"{bbox_str}\n")
            else:
                print(f"Invalid bbox format for image_id {image_id}: {bbox}")

# Function to process the CSV file and save bounding box data to text files
def process_csv(csv_file, folder):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image_id = row['image_id']
            bbox_data = row['bbox']
            save_bbox_to_text(image_id, bbox_data, folder)

# Main function
def main():
    csv_file = "/home/ubuntu/mmocr/coco_output_paulo.csv"  # Provide the path to your CSV file
    output_folder = "/home/ubuntu/mmocr/output_folder_coco"  # Specify the output folder where text files will be saved
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    process_csv(csv_file, output_folder)

if __name__ == "__main__":
    main()
