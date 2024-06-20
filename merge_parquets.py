import pyarrow.parquet as pq
import os
import pandas as pd
import pyarrow as pa

# data = pq.read_table("logofusion02/train/part-00001-tid-8393453412907680285-15e78f28-cb30-4bc5-8887-6f4364f8ce6d-95306-1-c000.snappy.parquet")
# print(data.num_rows)

# Function to merge Parquet files from a folder and remove duplicates based on asset_id
def merge_parquet_files(input_folder, output_file):
    # Read all Parquet files from the input folder
    parquet_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.parquet')]
    
    # Initialize an empty DataFrame to store the merged data
    merged_data = pd.DataFrame()

    # Read each Parquet file and append its data to the merged DataFrame
    for file in parquet_files:
        table = pq.read_table(file)
        df = table.to_pandas()
        merged_data = pd.concat([merged_data, df], ignore_index=True)
    
    # Count the number of duplicated rows
    num_duplicates = merged_data.duplicated(subset='uri').sum()
    
    # Remove duplicates based on the 'asset_id' column
    merged_data.drop_duplicates(subset='uri', inplace=True)
    
    # Convert the DataFrame back to a PyArrow table
    table = pa.Table.from_pandas(merged_data)
    
    # Write the merged data to a new Parquet file
    pq.write_table(table, output_file)
    
    # Get the number of rows in the final merged file
    num_rows_final = len(merged_data)
    
    return num_duplicates, num_rows_final

# Specify input folder containing Parquet files and output file path
input_folder = 'logo05/train/'
output_file = 'logo05/train/merged_file.parquet'

# Merge Parquet files and remove duplicates based on 'asset_id'
num_duplicates, num_rows_final = merge_parquet_files(input_folder, output_file)

print("Number of duplicated rows removed:", num_duplicates)
print("Number of rows in the final merged file:", num_rows_final)