import pandas as pd
from fastparquet import ParquetFile

df = pd.read_parquet('data/01_taxi_data_0322_0323_all_areas.parquet')


# getting only data from zone 70 --> nähester Area am Mean
grouped = df.loc[df['PULocationID'] == 70]

# print amount of rows of grouped
print(grouped.shape[0])


# sorting tpep_pickup_datetime
grouped = grouped.sort_values(by=['tpep_pickup_datetime'])

# reestting index
grouped = grouped.reset_index(drop=True)

grouped.to_parquet('data/02_timeseries_zone70.parquet', engine='fastparquet')
grouped.to_csv('data/02_timeseries_zone70.csv')