from matplotlib.pyplot import table
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from fastparquet import ParquetFile
import os


pqwriter = None


# Öffne die Eingabedateien.
file_location = '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/'
# input_files_22 = [
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-04.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-05.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-06.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-07.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-08.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-09.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-10.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-11.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-12.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-01.parquet']

input_files_23 =[
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-02.parquet',
# '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-03.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-04.parquet'
]

# Columns to drop
# columns_to_drop_22 = ['VendorID',
#                     'tpep_dropoff_datetime',
#                     'DOLocationID',
#                     'passenger_count',
#                     'trip_distance',
#                     'RatecodeID', 
#                     'store_and_fwd_flag', 
#                     'payment_type', 
#                     'fare_amount', 
#                     'extra', 
#                     'mta_tax', 
#                     'tip_amount', 
#                     'tolls_amount', 
#                     'improvement_surcharge', 
#                     'total_amount', 
#                     'congestion_surcharge',
#                     'airport_fee', 
#                     ]

# Columns to drop
columns_to_drop_23 = ['VendorID',
                    'tpep_dropoff_datetime',
                    'DOLocationID',
                    'passenger_count',
                    'trip_distance',
                    'RatecodeID', 
                    'store_and_fwd_flag', 
                    'payment_type', 
                    'fare_amount', 
                    'extra', 
                    'mta_tax', 
                    'tip_amount', 
                    'tolls_amount', 
                    'improvement_surcharge', 
                    'total_amount', 
                    'congestion_surcharge',
                    'Airport_fee', 
                    ]

data_frames = []

## Zwei Iterationen, da der Spaltename 'Airport_fee' in 22 und 23 unterschiedlich ist
# for files in input_files_22:
#     data = pq.read_table(files)
#     df = data.to_pandas()
#     df = df[df['passenger_count'] != 0] #lösche passenger_count = 0 zeilen
#     df.drop(columns=columns_to_drop_22, inplace=True) #lösche Spalten
#     data_frames.append(df)

##
for files in input_files_23:
    data = pq.read_table(files)
    df = data.to_pandas()
    df = df[df['passenger_count'] != 0] #lösche passenger_count = 0 zeilen
    df.drop(columns=columns_to_drop_23, inplace=True) #lösche Spalten
    data_frames.append(df)

## Merge all dataframes
merged_df = pd.concat(data_frames, ignore_index=True)

## Data not in 2022 are dropped
merged_df = merged_df[(merged_df['tpep_pickup_datetime'] > "2022-04-01 00:00:00")] #lösche alle Daten vor 2022-04-01
merged_df = merged_df[(merged_df['tpep_pickup_datetime'] < "2023-04-30 00:00:00")] #lösche alle Daten nach 2023-04-01

##Set index to tpep_pickup_datetime
#merged_df = merged_df.set_index('tpep_pickup_datetime')

## getting only data from zone 70 --> nähester Area am Mean
merged_df = merged_df.loc[merged_df['PULocationID'] == 70]


#################
# testset with 1h intervall
df60 = (pd.to_datetime(merged_df['tpep_pickup_datetime'], unit='H')
    .dt.floor('1H') 
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count')
)

# Erstellen Sie einen vollständigen Datumsbereich vom Start- bis zum Enddatum
full_date_range = pd.date_range(start=df60['date'].min(), end=df60['date'].max(), freq='H')

# Fehlende Werte mit 0 auffüllen
df60.set_index('date', inplace=True)
df60 = df60.reindex(full_date_range, fill_value=0).reset_index().rename(columns={'index': 'date'})

df60 = df60.sort_values(by='date', ascending=True)

df60.to_parquet('data/03_60min_testset.parquet', engine='fastparquet')

#################
# testset with 30min intervall

df30 = (pd.to_datetime(merged_df['tpep_pickup_datetime'])
    .dt.floor('30min')
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count')
)

# Erstellen Sie einen vollständigen Datumsbereich vom Start- bis zum Enddatum
full_date_range = pd.date_range(start=df30['date'].min(), end=df30['date'].max(), freq='30min')

# Fehlende Werte mit 0 auffüllen
df30.set_index('date', inplace=True)
df = df30.reindex(full_date_range, fill_value=0).reset_index().rename(columns={'index': 'date'})

df30 = df30.sort_values(by='date', ascending=True)

df30.to_parquet('data/03_30min_testset.parquet', engine='fastparquet')


#################
# testset with 15min intervall
df15 = (pd.to_datetime(merged_df['tpep_pickup_datetime'])
    .dt.floor('15min')
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count')
)

# Erstellen Sie einen vollständigen Datumsbereich vom Start- bis zum Enddatum
full_date_range = pd.date_range(start=df15['date'].min(), end=df15['date'].max(), freq='15min')

# Fehlende Werte mit 0 auffüllen
df15.set_index('date', inplace=True)
df15 = df15.reindex(full_date_range, fill_value=0).reset_index().rename(columns={'index': 'date'})

df15 = df15.sort_values(by='date', ascending=True)

df15.to_parquet('data/03_15min_testset.parquet', engine='fastparquet')



