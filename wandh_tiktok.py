import os
import subprocess
import pandas as pd
import json
from PIL import Image

# Read URIs from JSON file
json_file = './tiktok/tiktok.json'
with open(json_file, 'r') as f:
    data = json.load(f)
uris = [entry['data']['uri'] for entry in data]
asset_ids = [entry['id'] for entry in data]

# Process images referenced by URIs
output_directory = 'outputs_tiktok'
os.makedirs(output_directory, exist_ok=True)

# Initialize a list to store the image information
image_info = []

for i, (uri, asset_id) in enumerate(zip(uris, asset_ids), start=1):
    try:
        # Generate filename using asset ID
        image_filename = os.path.join(output_directory, f'{asset_id}.jpg')

        # Download object from S3 using aws s3 command
        subprocess.run(['aws', '--profile', 'saml', 's3', 'cp', uri, image_filename])

        # Get image dimensions
        with Image.open(image_filename) as img:
            width, height = img.size

        # Save image information
        image_info.append({'uri': uri, 'id': asset_id, 'width': width, 'height': height})
        print(f'Processed image {i}/{len(uris)}: {image_filename}')
    except Exception as e:
        print(f'Error processing image {i}/{len(uris)}: {e}')

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(image_info)

# Save DataFrame to CSV
csv_file_path = 'image_info.csv'
df.to_csv(csv_file_path, index=False)
