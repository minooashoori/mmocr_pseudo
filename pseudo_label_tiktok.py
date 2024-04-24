import os
import subprocess
import pandas as pd
import json
from mmocr.apis import MMOCRInferencer

# Read URIs from JSON file
json_file = 'tiktok.json'
with open(json_file, 'r') as f:
    data = json.load(f)
uris = [entry['data']['uri'] for entry in data]
asset_ids = [entry['id'] for entry in data]


# Initialize MMOCRInferencer
ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

# Process images referenced by URIs
output_directory = 'outputs_tiktok'
os.makedirs(output_directory, exist_ok=True)


for i, (uri, asset_id) in enumerate(zip(uris, asset_ids), start=1):
    try:
    
        # Generate filename using asset ID
        image_filename = os.path.join(output_directory, f'{asset_id}.jpg')

        # Download object from S3 using aws s3 command
        subprocess.run(['aws', '--profile', 'saml' , 's3', 'cp', uri, image_filename])

        # Run the model on the downloaded image
        a = ocr(image_filename, out_dir=output_directory, save_pred=True, return_vis=False)
        
        # Delete the downloaded image after processing
        os.remove(image_filename)
        print(f'Deleted image {i}/{len(uris)}: {image_filename}')
    except Exception as e:
        print(f'Error processing image {i}/{len(uris)}: {e}')

