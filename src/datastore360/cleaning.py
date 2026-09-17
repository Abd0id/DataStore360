import pandas as pd
import numpy as np


file_path = '../../data/raw/store-data-6aa6d7a3f171f140353680.csv'
df = pd.read_csv(file_path)

df_cleaning = df.drop_duplicates()

