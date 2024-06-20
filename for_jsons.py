import os
import json
import time
import numpy as np
from mmocr.utils.polygon_utils import poly2bbox

# Directory containing your JSON files
directory = 'a/'

# Initialize an empty list to store data from all files
combined_data = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as file:
            data = json.load(file)
            
            # Extract ID (filename) and creation time
            file_id = filename.split('.')[0]
            creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(os.path.join(directory, filename))))
            
            # Extract relevant data from the JSON
            predictions = data.get('output', {}).get('predictions', [])
            bbox = []
            det_polygons = []
            det_scores = []
            for prediction in predictions:
                polygons = prediction.get('det_polygons', [])
                scores = prediction.get('det_scores', [])
                det_polygons.extend(polygons)
                det_scores.extend(scores)
                for poly in polygons:
                    box = poly2bbox(poly)
                    box_list = box.tolist() if isinstance(box, np.ndarray) else box
                    bbox.append(box_list)
            
            # Create a new dictionary with all the information
            combined_entry = {
                "ID": file_id,
                "created_at": creation_time,
                "total_boxes": len(det_polygons),
                "bbox": bbox,
                "det_polygons": det_polygons,
                "det_scores": det_scores,
                "uri": data.get('uri', '')
            }
            
            # Append the entry to the combined data list
            combined_data.append(combined_entry)

# Alternatively, sort combined_data by creation time
combined_data_sorted = sorted(combined_data, key=lambda x: x["ID"])

# Write the combined data to a single JSON file
output_file = 'logofusion02_mmocr.json'
with open(output_file, 'w') as outfile:
    json.dump(combined_data_sorted, outfile, indent=4)

print(f"Combined data from {len(combined_data)} JSON files into {output_file}")
