import pandas as pd
from src.database import get_db_engine


def extract_csv_to_staging(file_path: str):
    """Reads raw CSV and loads it into the staging schema without modifications."""
    engine = get_db_engine()
    df_raw = pd.read_csv(file_path)

    # Loads into staging.superstore_raw
    df_raw.to_sql('superstore_raw', engine, schema='staging', if_exists='replace', index=False)

    return f"Successfully loaded {len(df_raw)} rows to staging."