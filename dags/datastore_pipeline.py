# dags/datastore_pipeline.py
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd
from src.cleaning import clean_and_transform


@dag(
    start_date=datetime(2026, 9, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['datastore360']
)
def datastore360_etl():
    @task
    def load_to_staging():
        # 1. Read raw data (assuming Docker volume mapped to /opt/airflow/data)
        df_raw = pd.read_csv('/opt/airflow/data/store_data.csv')

        # 2. Connect to Postgres
        hook = PostgresHook(postgres_conn_id='DATASTORE_DB')
        engine = hook.get_sqlalchemy_engine()

        # 3. Dump raw data into staging schema
        # (Ensure you created the 'staging' schema in your include/sql scripts)
        df_raw.to_sql('superstore_raw', engine, schema='staging', if_exists='replace', index=False)

        return "Staging load complete"

    @task
    def transform_and_load_to_core(staging_status):
        # 1. Pull data from staging
        hook = PostgresHook(postgres_conn_id='DATASTORE_DB')
        engine = hook.get_sqlalchemy_engine()
        df_raw = pd.read_sql("SELECT * FROM staging.superstore_raw", engine)

        # 2. Run your src/cleaning.py logic
        customers, products, orders = clean_and_transform(df_raw)

        # 3. Load into core schema
        # (Ensure you created the 'core' schema in your include/sql scripts)
        customers.rename(columns=lambda x: x.replace(' ', '').lower(), inplace=True)
        customers.to_sql('customers', engine, schema='core', if_exists='append', index=False)

        products.rename(columns=lambda x: x.replace(' ', '').lower(), inplace=True)
        products.to_sql('products', engine, schema='core', if_exists='append', index=False)

        orders.rename(columns=lambda x: x.replace(' ', '').lower(), inplace=True)
        orders.to_sql('orders', engine, schema='core', if_exists='append', index=False)

    # Define task dependencies
    staging_complete = load_to_staging()
    transform_and_load_to_core(staging_complete)


# Instantiate the DAG
dag = datastore360_etl()