from matplotlib.pyplot import table
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from fastparquet import ParquetFile


pqwriter = None


# Öffne die Eingabedateien.
input_files = ["raw/2022 TLC data/yellow_tripdata_2022-01.parquet","raw/2022 TLC data/yellow_tripdata_2022-02.parquet", "raw/2022 TLC data/yellow_tripdata_2022-03.parquet", "raw/2022 TLC data/yellow_tripdata_2022-04.parquet", "raw/2022 TLC data/yellow_tripdata_2022-05.parquet",
                    "raw/2022 TLC data/yellow_tripdata_2022-06.parquet", "raw/2022 TLC data/yellow_tripdata_2022-07.parquet", "raw/2022 TLC data/yellow_tripdata_2022-08.parquet", "raw/2022 TLC data/yellow_tripdata_2022-09.parquet", "raw/2022 TLC data/yellow_tripdata_2022-10.parquet",
                    "raw/2022 TLC data/yellow_tripdata_2022-11.parquet", "raw/2022 TLC data/yellow_tripdata_2022-12.parquet"]



for files in input_files:
    data = pq.read_table(files).drop_columns(['VendorID','DOLocationID', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance', 'RatecodeID', 'store_and_fwd_flag', 'payment_type', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 'congestion_surcharge', 'airport_fee'])      
    
    if pqwriter is None:
        pqwriter = pq.ParquetWriter("data/2022_taxi_rides_raw.parquet", data.schema, version='1.0')


    # Schreibe die Daten aus den Eingabedateien in die Ausgabedatei.
    pqwriter.write_table(data)

    # Schließe die Ausgabedatei.


pqwriter.close()


# Data handling

df = pd.read_parquet('data/2022_taxi_rides_raw.parquet')


df = df.loc[df['PULocationID'] == 4] # get only zoneID 4


df = (pd.to_datetime(df['tpep_pickup_datetime'], unit='s')
    .dt.floor('30min') 
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count'))

print(df)

df = df.sort_values(by='date', ascending=True)

#df = df.set_index('date').to_period('H').sort_index(ascending=True)

#df.sort_values(by=df.index, ascending=True, inplace=True)


print(df.dtypes)

df = df[(df['date'] > "2022-01-01 00:00:00")]
df = df[(df['date'] < "2023-01-01 00:00:00")]

df = df.set_index('date')

print(df.head())

df.to_parquet('data/2022_taxi_rides.parquet', engine='fastparquet')



