import pandas as pd
import os

# Read Parquet file
# df = pd.read_parquet('/home/ubuntu/logo_05_idx_0000.parquet')

# # Save DataFrame as CSV
# df.to_csv('logo05_test.csv', index=False)

# Save DataFrame as CSV
df = pd.read_json('/home/ubuntu/mmocr/COCO_Text_2.json')

df.to_csv('coco_raw_paulo.csv', index=False)


# Define the directory paths
# parquet_folder = './parquets/'
# csv_folder = './csvs2/'

# # Create the CSV folder if it doesn't exist
# if not os.path.exists(csv_folder):
#     os.makedirs(csv_folder)

# # Initialize index for numbering CSV files
# csv_index = 1

# # Iterate over all files in the Parquet folder
# for filename in os.listdir(parquet_folder):
#     if filename.endswith('.parquet'):
#         # Read the Parquet file into a DataFrame
#         df = pd.read_parquet(os.path.join(parquet_folder, filename))
        
#         # Define the CSV filename with consecutive numbering
#         csv_filename = os.path.join(csv_folder, f'{csv_index}.csv')
        
#         # Save the DataFrame as a CSV file
#         df.to_csv(csv_filename, index=False)
        
#         print(f"Saved {filename} as {csv_filename}")
        
#         # Increment the index for the next CSV file
#         csv_index += 1
