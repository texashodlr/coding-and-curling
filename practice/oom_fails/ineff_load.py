from memory_profiler import profile
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, filename='pipeline.log')

@profile
def load_data(file_path):
    df = pd.read_csv(file_path)
    logging.info(f"Loaded {len(df)} rows, memory usage: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    return df

@profile
def inefficient_processing(file_path):
    df = pd.read_csv(file_path)
    for i in range(len(df)):
        df.iloc[i, df.columns.get_loc('vin')] *= 2
    return df

@profile
def efficient_processing(file_path):
    df = pd.read_csv(file_path, usecols=['dealer_id', 'vin', 'build_date'])
    df['vin'] = df['vin'] * 2
    logging.info(f"Processed {len(df)} rows, memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    return df

if __name__ == '__main__':
    df = load_data('data.csv')
    df = inefficient_processing('data.csv')
    df = efficient_processing('data.csv')
