import pandas as pd

# Read the first CSV file into a DataFrame
df1 = pd.read_csv('./logo05/train/logo_05_idx_60000_flt.csv')

# Read the second CSV file into a DataFrame
df2 = pd.read_csv('./logo05_mmocr_idx_60000_with_uri.csv')

# # Check column names of both DataFrames
# print("Columns in df1:", df1.columns)
# print("Columns in df2:", df2.columns)

# Perform an anti-join to get rows in df1 that don't have the same asset_id as df2
anti_join_df = df2[~df2['uri'].isin(df1['uri'])]

# Get the number of rows in the anti-join DataFrame
num_rows = len(anti_join_df)
print("Number of rows in file 1 that don't have the same asset_id as file 2:", num_rows)

# Save the anti-join DataFrame as a CSV file
anti_join_df.to_csv('60000_added.csv', index=False)