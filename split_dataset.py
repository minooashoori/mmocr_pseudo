import pandas as pd
from sklearn.model_selection import train_test_split

# Read the Parquet file
df = pd.read_parquet('logodet3k/logodet3k_val_flt_cleared.parquet')

# Split the DataFrame: 80% for training and 20% for testing
train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)

# Save the 80% data to a new Parquet file
train_df.to_parquet('logodet3k/val_excess_file.parquet')

# Save the 20% data to another Parquet file
test_df.to_parquet('logodet3k/val_file.parquet')
