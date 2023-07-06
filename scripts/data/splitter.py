import pandas as pd
import math

# Read the original dataset
dataset = pd.read_csv('dataset_A.csv')

# Split the dataset into smaller chunks of 101 rows
chunk_size = 101
num_chunks = math.ceil(len(dataset) / chunk_size)

# Split the dataset and save into smaller CSV files
for i in range(num_chunks):
    start_index = i * chunk_size
    end_index = (i + 1) * chunk_size

    # Extract the chunk from the dataset
    chunk = dataset.iloc[start_index:end_index]

    # Generate the filename for the chunk
    filename = f'batches/batch_{i + 1}.csv'

    # Save the chunk to a CSV file
    chunk.to_csv(filename, index=False)

    print(f'Saved {filename} with {len(chunk)} rows')

print('Dataset splitting complete.')
