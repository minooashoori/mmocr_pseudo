import os
import subprocess
import pandas as pd

# Read URIs and asset IDs from CSV file
csv_file = 'val.csv'
df = pd.read_csv(csv_file)
uris = df['path']
asset_ids = df['asset']

# Define output directory
output_directory = 'logodet3k_val'
os.makedirs(output_directory, exist_ok=True)

# Iterate over URIs and download images
for i, (uri, asset_id) in enumerate(zip(uris, asset_ids), start=1):
    try:
        # Construct S3 URI
        s3_uri = f's3://mls.us-east-1.innovation/pdacosta/data/logodet_3k/{uri}'

        # Generate filename using asset ID
        image_filename = os.path.join(output_directory, f'{asset_id}.jpg')

        # Download object from S3 using aws s3 command
        subprocess.run(['aws', '--profile', 'saml', 's3', 'cp', s3_uri, image_filename])

        print(f'Downloaded image {i}/{len(uris)}: {image_filename}')
    except Exception as e:
        print(f'Error downloading image {i}/{len(uris)}: {e}')
