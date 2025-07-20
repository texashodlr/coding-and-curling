import pandas as pd
import gc
import os
import glob

def leaky_loop(file_path):
    results = []
    for file in file_path:
        df = pd.read_csv(file)
        results.append(df)
    return results

def fixed_loop(file_paths):
    results = []
    for file in file_paths:
        df = pd.read_csv(file, usecols=['brand_name', 'model_id'])
        results.append(df.sum())
        del df
        gc.collect()
        logging.info(f"Processed {file}, memory freed")
    return results

csv_files = glob.glob('data/*.csv')

df = leaky_loop(csv_files)

del df
gc.collect()

df = fixed_loop(csv_files)

"""
Batched processing:

def process_in_batches(file_path, chunk_size=10000):
    chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)
    results = []
    for i, chunk in enumerate(chunk_iter):
        # Process chunk (e.g., filter rows, compute aggregates)
        chunk = chunk[chunk['value'] > 0]
        results.append(chunk[['id', 'value']].mean())
        logging.info(f"Processed chunk {i}, memory: {chunk.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    return pd.concat(results).mean()


"""
