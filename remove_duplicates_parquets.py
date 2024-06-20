import os
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


# Function to remove rows from file m that have the same asset_id as any of the other Parquet files
def remove_duplicates(single_file, other_files, output_file):
    # Read file m
    single_data = pq.read_table(single_file).to_pandas()
    
    # Initialize an empty DataFrame to store data from other files
    other_data = pd.DataFrame()

    # Read each other Parquet file and append its data to the other_data DataFrame
    for file in other_files:
        data = pq.read_table(file).to_pandas()
        other_data = pd.concat([other_data, data], ignore_index=True)
    
    # Get a list of unique asset_ids from other_data
    unique_asset_ids = set(other_data['uri'])
    
    # Remove rows from m_data that have the same asset_id as any of the other files
    num_deleted_rows = single_data.shape[0] - single_data[~single_data['uri'].isin(unique_asset_ids)].shape[0]
    filtered_data = single_data[~single_data['uri'].isin(unique_asset_ids)]
    
    # Convert filtered data back to PyArrow table
    filtered_table = pa.Table.from_pandas(filtered_data)
    
    # Write the filtered data to a new Parquet file
    pq.write_table(filtered_table, output_file)
    
    return num_deleted_rows

# Specify file m and other Parquet files
single_file = 'logofusion02/train&val/merged_file.parquet'
other_files = ['logo_05_idx_00000.parquet', 'logo_05_idx_10000.parquet', 'logo_05_idx_20000.parquet', 'logo_05_idx_30000.parquet', 'logo_05_idx_40000.parquet', 'logo_05_idx_50000.parquet', 'logo_05_idx_60000.parquet']
output_file = 'logofusion02/logofusion02_filtered.parquet'

# Remove rows from file m that have the same asset_id as any of the other Parquet files
num_deleted_rows = remove_duplicates(single_file, other_files, output_file)

print("Number of deleted rows from single file:", num_deleted_rows)
