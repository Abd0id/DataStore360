import pandas as pd
import numpy as np
import hashlib



csv_path = "../../data/raw/store-data-6aa6d7a3f171f140353680.csv"

df = pd.read_csv(csv_path)

str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda s: s.str.strip())

df["Segment"] = df["Segment"].replace({"Consumerr": "Consumer"})
df["Segment"] = df["Segment"].replace({"Home Ofice": "Home Office"})
df["Segment"] = df["Segment"].replace({"Corporrate": "Corporate"})


df["Customer Name"] = df["Customer Name"].str.strip().str.title()
df["Category"] = df["Category"].str.strip().str.title()
df["Segment"] = df["Segment"].str.strip().str.title()
df["State"] = df["State"].str.strip().str.title()
df["City"] = df["City"].str.strip().str.title()

df = df.drop_duplicates()

for column in ['Order Date', 'Ship Date']:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')

if {'Order Date', 'Ship Date'}.issubset(df.columns):
    invalid_dates = df[
        df['Order Date'].notna() &
        df['Ship Date'].notna() &
        (df['Ship Date'] < df['Order Date'])
    ]
    df = df.drop(invalid_dates.index)

df['Customer Name'] = df['Customer Name'].fillna(
    df.groupby('Customer ID')['Customer Name'].transform('first')
)

df['Postal Code'] = df['Postal Code'].fillna(
    df.groupby('City')['Postal Code'].transform('first')
)


df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df.dropna(subset = ['Shipping Days'])


median_days = df.groupby("Ship Mode")["Shipping Days"].median()
median_days = pd.to_timedelta(df["Ship Mode"].map(median_days))

df["Ship Date"] = np.where(df["Shipping Days"] > 90, df["Order Date"] + median_days, df["Ship Date"])


median_days = df.groupby("Ship Mode")["Shipping Days"].median()

def find_mode(days):
    difference = (median_days - days).abs()
    return difference.idxmin()

missing = df["Ship Mode"].isna()

df.loc[missing, "Ship Mode"] = df.loc[missing, "Shipping Days"].apply(find_mode)

df["Quantity"] = df['Quantity'].fillna(df['Quantity'].mode().iloc[0])
df = df.dropna(subset = ['Sales'])

df["Discount"] = df["Discount"].fillna(df.groupby(["Product ID", "Sales"])["Discount"].transform(lambda x: x.median()))
df = df[~((df['Discount'] < 0) | (df['Discount'] > 1))]

df["Quantity"] = df["Quantity"].fillna(
    df.groupby(["Product ID", "Sales"])["Quantity"].transform(lambda x: x.median())
)

df["Quantity"] = df["Quantity"].round().astype(int)

df["Sales"] = df["Sales"].fillna(df.groupby(["Product ID", "Quantity"])["Sales"].transform(lambda x: x.median()))


df = df.drop_duplicates()
df = df.dropna(subset=['Customer Name'])
df = df[df['Quantity'] > 0]
df = df.drop(columns= 'Profit')

def hash_name(name):
    return hashlib.sha256(name.encode("utf-8")).hexdigest()

df["Customer Name"] = df["Customer Name"].apply(hash_name)



df.to_csv("../../data/processed/store-data-clean.csv", index=False)
