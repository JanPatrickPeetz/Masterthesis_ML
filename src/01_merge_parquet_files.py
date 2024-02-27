from matplotlib.pyplot import table
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from fastparquet import ParquetFile
import os


pqwriter = None


# Öffne die Eingabedateien.
file_location = '/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/'
input_files_22 = [
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-04.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-05.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-06.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-07.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-08.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-09.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-10.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-11.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2022 TLC data/yellow_tripdata_2022-12.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-01.parquet']

input_files_23 =[
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-02.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-03.parquet',
'/Users/paddy/Documents/GitHub/Masterthesis_ML/raw/2023 TLC data/yellow_tripdata_2023-04.parquet'
]

# Columns to drop
columns_to_drop_22 = ['VendorID',
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
                    'airport_fee', 
                    ]

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
for files in input_files_22:
    data = pq.read_table(files)
    df = data.to_pandas()
    df = df[df['passenger_count'] != 0] #lösche passenger_count = 0 zeilen
    df.drop(columns=columns_to_drop_22, inplace=True)
    data_frames.append(df)

##
for files in input_files_23:
    data = pq.read_table(files)
    df = data.to_pandas()
    df = df[df['passenger_count'] != 0] #lösche passenger_count = 0 zeilen
    df.drop(columns=columns_to_drop_23, inplace=True)
    data_frames.append(df)

## Merge all dataframes
merged_df = pd.concat(data_frames, ignore_index=True)

## Data not in 2022 are dropped
merged_df = merged_df[(merged_df['tpep_pickup_datetime'] > "2022-04-01 00:00:00")] #lösche alle Daten vor 2022-03-01 00:00:00
merged_df = merged_df[(merged_df['tpep_pickup_datetime'] < "2023-05-01 00:00:00")] #lösche alle Daten nach 2023-03-30 00:00:00

##Set index to tpep_pickup_datetime
#merged_df = merged_df.set_index('tpep_pickup_datetime')


## getting only data from zone 70 --> nähester Area am Mean
merged_df = merged_df.loc[merged_df['PULocationID'] == 70]

#sort by time
merged_df = merged_df.sort_values(by='tpep_pickup_datetime', ascending=True)

print(merged_df.tail())

## Define output path
output_file_path = '/Users/paddy/Documents/GitHub/Masterthesis_ML/data/01_all_month.parquet'

## Write to parquet
merged_df.to_parquet(output_file_path, engine='fastparquet')
merged_df.to_csv('data_01.csv')






