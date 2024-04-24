import os
import subprocess
import pandas as pd
import json
from mmocr.apis import MMOCRInferencer

# Read URIs from CSV file
csv_file = 'train.csv'
df = pd.read_csv(csv_file)
uris = df['path']
asset_ids = df['asset']

# Initialize MMOCRInferencer
ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

# Process images referenced by URIs
output_directory = 'outputs_logodet3k'
os.makedirs(output_directory, exist_ok=True)


for i, (uri, asset_id) in enumerate(zip(uris, asset_ids), start=1):
    try:
        # Construct S3 URI
        s3_uri = f's3://mls.us-east-1.innovation/pdacosta/data/logodet_3k/{uri}'

        # Generate filename using asset ID
        image_filename = os.path.join(output_directory, f'{asset_id}.jpg')

        # Download object from S3 using aws s3 command
        subprocess.run(['aws', '--profile', 'saml' , 's3', 'cp', s3_uri, image_filename])

        # Run the model on the downloaded image
        a = ocr(image_filename, out_dir=output_directory, save_pred=True, return_vis=False)


        # Delete the downloaded image after processing
        os.remove(image_filename)
        print(f'Deleted image {i}/{len(uris)}: {image_filename}')
    except Exception as e:
        print(f'Error processing image {i}/{len(uris)}: {e}')

