import os
import subprocess
import pyarrow.parquet as pq
from mmocr.apis import MMOCRInferencer

# Read the Parquet file and extract URIs
parquet_file = 'logo_05_idx_10000.parquet'
parquet_table = pq.read_table(parquet_file)
uri_column = parquet_table['uri']
uris = uri_column.to_pylist()
asset_ids = parquet_table['asset_id'].to_pylist()

# Initialize MMOCRInferencer
ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

# Process images referenced by URIs
output_directory = 'outputs_10000'
os.makedirs(output_directory, exist_ok=True)

for i, (uri, asset_id) in enumerate(zip(uris, asset_ids), start=1):
    try:
        # Construct S3 URI
        s3_uri = f's3://{uri}'

        # Generate filename using asset ID
        image_filename = os.path.join(output_directory, f'{asset_id}.jpg')

        # Download object from S3 using aws s3 command
        subprocess.run(['aws', '--profile', 'saml' , 's3', 'cp', s3_uri, image_filename])

        # Run the model on the downloaded image
        a = ocr(image_filename, out_dir=output_directory, save_pred=True, return_vis=False)

        print(f'Processed image {i}/{len(uris)}: {s3_uri}')

        # Delete the downloaded image after processing
        os.remove(image_filename)
        print(f'Deleted image {i}/{len(uris)}: {image_filename}')
    except Exception as e:
        print(f'Error processing image {i}/{len(uris)}: {e}')
