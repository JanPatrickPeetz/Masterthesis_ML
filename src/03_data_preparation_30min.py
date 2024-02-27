from matplotlib.pyplot import table
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from fastparquet import ParquetFile


# Data handling
df = pd.read_parquet('data/01_taxi_data_0322_0323.parquet')

#delete data before april 2022
df = df[df['tpep_pickup_datetime'] >= '2022-04-01 00:00:00']



df = (pd.to_datetime(df['tpep_pickup_datetime'])
    .dt.floor('30min')
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count')
)

# Erstellen Sie einen vollständigen Datumsbereich vom Start- bis zum Enddatum
full_date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='30min')

# Fehlende Werte mit 0 auffüllen
df.set_index('date', inplace=True)
df = df.reindex(full_date_range, fill_value=0).reset_index().rename(columns={'index': 'date'})

#
df = df.sort_values(by='date', ascending=True)


df.to_parquet('data/03_30min_dataset.parquet', engine='fastparquet')
df.to_csv('data/03_30min_dataset.csv')