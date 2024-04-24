import pyarrow.parquet as pq

# Read the Parquet file
parquet_file = 'logo_05_idx_00000.parquet'
parquet_table = pq.read_table(parquet_file)

# Get the `uri` column
uri_column = parquet_table['uri']

# # Convert the uri_column to a list of Python objects
# uri_list = uri_column.to_pylist()

# # Decode the byte array to get the URLs
# urls = [uri.decode('utf-8') for uri in uri_column[:10]]

# Print the first 10 URLs
# for url in urls:
#     print(url)
print(uri_column[:1])