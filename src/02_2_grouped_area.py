import pandas as pd
from fastparquet import ParquetFile
import numpy as np

df = pd.read_parquet('data/01_taxi_data_0322_0323_all_areas.parquet')


##grouping
grouped = df.groupby('PULocationID', dropna=False).size().reset_index(name='counts')
grouped.set_index('PULocationID')



#Reindex grouped mit missing areas
grouped = grouped.set_index('PULocationID')
grouped = grouped.reindex(np.arange(1,264), fill_value=0)
grouped = grouped.reset_index()
grouped = grouped.rename(columns={'index':'PULocationID'})




# save
grouped.to_parquet('data/02_grouped_area_all_areas.parquet', engine='fastparquet')
grouped.to_csv('data/02_grouped_area_all_areas.csv')