import pandas as pd
import numpy as np


csv_path = "../../data/raw/store-data-6aa6d7a3f171f140353680.csv"

df = pd.read_csv(csv_path)

str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda s: s.str.strip())

df["Category"] = df["Category"].str.lower()
df["Segment"] = df["Segment"].str.lower()

df["Segment"] = df["Segment"].replace({"Consumerr": "Consumer"})

# print(df["Segment"].unique())
