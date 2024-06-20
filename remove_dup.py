import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("merged_merged_data.csv")

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Save the DataFrame to a new CSV file
df.to_csv("merged_merged_2.csv", index=False)
