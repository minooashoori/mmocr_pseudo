# import os
# import subprocess
# import pyarrow.parquet as pq
# from mmocr.apis import MMOCRInferencer

# # Read the Parquet file and extract URIs
# parquet_file = 'logofusion02/logofusion02_filtered.parquet'
# parquet_table = pq.read_table(parquet_file)
# uri_column = parquet_table['uri']
# uris = uri_column.to_pylist()
# asset_ids = parquet_table['asset_id'].to_pylist()

# # Initialize MMOCRInferencer
# ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

# # Process images referenced by URIs
# output_directory = 'outputs_logofusion'
# os.makedirs(output_directory, exist_ok=True)

# # Define batch size
# batch_size = 500

# # Split URIs and asset IDs into batches
# uri_batches = [uris[i:i+batch_size] for i in range(0, len(uris), batch_size)]
# asset_id_batches = [asset_ids[i:i+batch_size] for i in range(0, len(asset_ids), batch_size)]

# for batch_num, (uri_batch, asset_id_batch) in enumerate(zip(uri_batches, asset_id_batches), start=1):
#     try:
#         # Construct S3 URIs and filenames for the batch
#         s3_uris = [f's3://{uri}' for uri in uri_batch]
#         image_filenames = [os.path.join(output_directory, f'{asset_id}.jpg') for asset_id in asset_id_batch]

#         # Download objects from S3 using aws s3 command and print the index
#         for i, (s3_uri, image_filename) in enumerate(zip(s3_uris, image_filenames), start=1):
#             print(f'Downloading image {i}/{len(uri_batch)} in batch {batch_num}/{len(uri_batches)}')
#             subprocess.run(['aws', '--profile', 'saml' , 's3', 'cp', s3_uri, image_filename])

#         # Run the model on the downloaded images
#         for i, (s3_uri, image_filename) in enumerate(zip(s3_uris, image_filenames), start=1):
#             a = ocr(image_filename, out_dir=output_directory, save_pred=True, return_vis=False)
#             print(f'Processed image {i}/{len(uri_batch)} in batch {batch_num}/{len(uri_batches)}: {s3_uri}')

#             # Delete the downloaded image after processing
#             os.remove(image_filename)
#             print(f'Deleted image {i}/{len(uri_batch)} in batch {batch_num}/{len(uri_batches)}: {image_filename}')
#     except Exception as e:
#         print(f'Error processing batch {batch_num}/{len(uri_batches)}: {e}')
import os
import subprocess
import pyarrow.parquet as pq
from mmocr.apis import MMOCRInferencer
import json

# Read the Parquet file and extract URIs
parquet_file = 'logofusion02_filtered.parquet'
parquet_table = pq.read_table(parquet_file)
uri_column = parquet_table['uri']
uris = uri_column.to_pylist()
asset_ids = parquet_table['asset_id'].to_pylist()

# Initialize MMOCRInferencer
ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

# Process images referenced by URIs
output_directory = 'outputs_logofusion'
os.makedirs(output_directory, exist_ok=True)

# Define batch size
batch_size = 500

# Split URIs and asset IDs into batches
uri_batches = [uris[i:i+batch_size] for i in range(0, len(uris), batch_size)]
asset_id_batches = [asset_ids[i:i+batch_size] for i in range(0, len(asset_ids), batch_size)]

for batch_num, (uri_batch, asset_id_batch) in enumerate(zip(uri_batches, asset_id_batches), start=1):
    try:
        # Construct S3 URIs and filenames for the batch
        s3_uris = [f's3://{uri}' for uri in uri_batch]
        image_filenames = [os.path.join(output_directory, f'{asset_id}.jpg') for asset_id in asset_id_batch]

        # Download objects from S3 using aws s3 command and print the index
        for i, (s3_uri, image_filename, asset_id) in enumerate(zip(s3_uris, image_filenames, asset_id_batch), start=1):
            print(f'Downloading image {i}/{len(uri_batch)} in batch {batch_num}/{len(uri_batches)}')
            subprocess.run(['aws', '--profile', 'saml' , 's3', 'cp', s3_uri, image_filename])

        # Run the model on the downloaded images
        for i, (s3_uri, image_filename, asset_id) in enumerate(zip(s3_uris, image_filenames, asset_id_batch), start=1):
            try:
                # Run the OCR
                output = ocr(image_filename, save_pred=False, return_vis=False)
                
                # Create a dictionary to hold both URI and output
                result = {'uri': s3_uri, 'output': output}
                
                # Create the 'a' folder if it doesn't exist
                os.makedirs('a', exist_ok=True)
                
                # Create the file path for the JSON file using the asset_id
                json_filename = os.path.join('a', f'{asset_id}.json')
                
                # Save the result as JSON in the 'a' folder
                with open(json_filename, 'w') as json_file:
                    json.dump(result, json_file)
                
                print(f'Processed image {i}/{len(uri_batch)} in batch {batch_num}/{len(uri_batches)}: {s3_uri}')
            except Exception as e:
                print(f'Error processing image {i}/{len(uri_batch)} in batch {batch_num}/{len(uri_batches)}: {e}')
    except Exception as e:
        print(f'Error processing batch {batch_num}/{len(uri_batches)}: {e}')





