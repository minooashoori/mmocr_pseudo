import pandas as pd
import os

# Read the first CSV file into a DataFrame
df1 = pd.read_csv('image_dimensions.csv')

# Initialize a list to store DataFrames
merged_dfs = []

# List of filenames for the second CSV files
csv_filenames = [filename for filename in os.listdir('csvs') if filename.endswith('.csv')]

# Merge each CSV file with df1 and store in a list
for filename in csv_filenames:
    # Read the CSV file into a DataFrame
    df2 = pd.read_csv(os.path.join('csvs', filename))    
    # df1['ID'] = df1['ID'].astype(str)
    # df2['asset_id'] = df2['asset_id'].astype(str)
    # Merge the two DataFrames based on a common column ('uri' in this case), using a left join
    merged_df = pd.merge(df1, df2, how='outer', left_on='id', right_on='image_id')
    
    # Append the merged DataFrame to the list
    merged_dfs.append(merged_df)

    # Get the number of merged rows
    num_merged_rows = merged_df.shape[0]
    print(f"Number of merged rows for {filename}: {num_merged_rows}")

# Concatenate all DataFrames in the list
concatenated_df = pd.concat(merged_dfs, ignore_index=True)

# Save the concatenated DataFrame as a CSV file
concatenated_df.to_csv('cocotext_ias.csv', index=False)
# concatenated_df.to_parquet('merged_merged_data.parquet', index=False)

# Print the total number of rows in the first DataFrame
print("Number of rows in the first DataFrame:", len(df1))

# Print the total number of rows in the concatenated DataFrame
print("Total number of rows in the concatenated DataFrame:", concatenated_df.shape[0])

