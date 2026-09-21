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
        df_raw = pd.read_csv('/opt/airflow/data/store_data.csv')

        return "Staging load complete"


dag = datastore360_etl()