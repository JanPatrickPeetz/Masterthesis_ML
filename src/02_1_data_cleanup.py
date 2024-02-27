import pandas as pd

df = pd.read_parquet('data/01_2022_taxi_rides_raw.parquet')

#df = data.drop(['VendorID', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance', 'RatecodeID', 'store_and_fwd_flag', 'payment_type', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 'congestion_surcharge', 'airport_fee'], axis=1)

## Data not in 2022 are dropped
df = df[(df['tpep_pickup_datetime'] > "2022-01-01 00:00:00")]
df = df[(df['tpep_pickup_datetime'] < "2023-01-01 00:00:00")]

## data that contain passenger_count = 0 are dropped
df = df.loc[df['passenger_count'] != 0]


#df = df.set_index('tpep_pickup_datetime')

df.to_parquet('data/02_2022_taxi_rides.parquet', engine='fastparquet')
