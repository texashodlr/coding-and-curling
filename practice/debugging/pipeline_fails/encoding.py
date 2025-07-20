import pandas as pd
import charset_normalizer
import logging
logging.basicConfig(level=logging.INFO, filename='ingestion.log')

with open('data.csv', 'rb') as f:
    result = charset_normalizer.detect(f.read())
    encoding = result['encoding']
    logging.info(f"Detected encoding: {encoding}")

df = pd.read_csv('data.csv', encoding=encoding, on_bad_lines='warn')
print(df.head())
