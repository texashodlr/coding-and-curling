from memory_profiler import profile
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, filename='pipeline.log')

@profile
def load_data(file_path):
    df = pd.read_csv(file_path)
    logging.info(f"Loaded {len(df)} rows, memory usage: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    return df

if __name__ == '__main__':
    df = load_data('data.csv')

"""

import psutil
def log_memory():
    process = psutil.Process()
    mem = process.memory_info().rss / 1e6  # Memory in MB
    logging.info(f"Current memory usage: {mem:.2f} MB")

"""
