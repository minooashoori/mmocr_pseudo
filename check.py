import pandas as pd

# Read the first CSV file into a DataFrame
df1 = pd.read_csv('logo_05_idx_00000.csv')

# Read the second CSV file into a DataFrame
df2 = pd.read_csv('logo05_mmocr_idx_00000.csv')

# Specify the column names you want to compare
column1 = 'asset_id'  # Change 'column_name1' to the actual column name in file1.csv
column2 = 'ID'  # Change 'column_name2' to the actual column name in file2.csv

# Check if there are any matching values between the two columns
matching_values = df1[column1].isin(df2[column2])

# Count the number of matching values
num_matches = matching_values.sum()

# Print the result
print(f"There are {num_matches} matching values between the two columns.")
