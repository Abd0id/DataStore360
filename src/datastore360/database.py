from airflow.providers.postgres.hooks.postgres import PostgresHook

def get_db_engine():
    """Retrieves the SQLAlchemy engine connected to the Postgres database."""
    # 'DATASTORE_DB' must match the connection name in your docker-compose or Airflow UI
    hook = PostgresHook(postgres_conn_id='DATASTORE_DB')
    return hook.get_sqlalchemy_engine()