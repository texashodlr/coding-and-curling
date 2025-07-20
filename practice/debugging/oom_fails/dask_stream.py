import dask.dataframe as dd
import logging

def process_with_dask(file_path):
    # Load CSV as Dask DataFrame (lazy loading)
    ddf = dd.read_csv(file_path, usecols=['vin', 'model_year', 'prefix'], dtype={'model_year': 'float64'})
    # Perform computation out-of-core
    result = ddf[ddf['model_year'] > 0]['model_year'].mean().compute()
    logging.info(f"Dask computed mean: {result}")
    return result

result = process_with_dask('data.csv')
