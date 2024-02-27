from matplotlib.pyplot import table
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from fastparquet import ParquetFile


# Data handling
df = pd.read_parquet('data/01_all_month.parquet')


df = (pd.to_datetime(df['tpep_pickup_datetime'], unit='H')
    .dt.floor('1H') 
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count')
)

# Erstellen Sie einen vollständigen Datumsbereich vom Start- bis zum Enddatum
full_date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='H')

# Fehlende Werte mit 0 auffüllen
df.set_index('date', inplace=True)
df = df.reindex(full_date_range, fill_value=0).reset_index().rename(columns={'index': 'date'})


df = df.sort_values(by='date', ascending=True).reindex()

print(df.tail())


df.to_parquet('data/03_032022_032023_taxi_rides.parquet', engine='fastparquet')
df.to_csv('data/03_2022_23_taxi_rides.csv')
