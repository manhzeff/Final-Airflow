import os
import glob
import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from sqlalchemy import create_engine

class StageToPostgresOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 table="",
                 data_path="",
                 *args, **kwargs):

        super(StageToPostgresOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.data_path = data_path

    def execute(self, context):
        postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn_object = postgres_hook.get_connection(self.postgres_conn_id)
        conn_uri = (
            f"postgresql://{conn_object.login}:{conn_object.password}"
            f"@{conn_object.host}:{conn_object.port}/{conn_object.schema}"
        )
        engine = create_engine(conn_uri)

        self.log.info(f"Clearing data from destination PostgreSQL table: {self.table}")
        postgres_hook.run(f"DELETE FROM {self.table}")

        self.log.info(f"Staging data from {self.data_path} to {self.table} table")

        all_files = []
        for root, dirs, files in os.walk(self.data_path):
            files = glob.glob(os.path.join(root,'*.json'))
            for f in files:
                all_files.append(os.path.abspath(f))

        self.log.info(f"Found {len(all_files)} files to process.")

        if not all_files:
            self.log.warning(f"No files found in {self.data_path}. Skipping task.")
            return

        df = pd.concat((pd.read_json(f, lines=True) for f in all_files), ignore_index=True)

        if self.table == 'staging_events':
            self.log.info("Renaming columns for staging_events table")
            column_map = {
                'artist': 'artist', 'auth': 'auth', 'firstName': 'firstname', 'gender': 'gender',
                'itemInSession': 'iteminsession', 'lastName': 'lastname', 'length': 'length',
                'level': 'level', 'location': 'location', 'method': 'method', 'page': 'page',
                'registration': 'registration', 'sessionId': 'sessionid', 'song': 'song',
                'status': 'status', 'ts': 'ts', 'userAgent': 'useragent', 'userId': 'userid'
            }
            df.rename(columns={k: v for k, v in column_map.items() if k in df.columns}, inplace=True)
            

            df['userid'] = pd.to_numeric(df['userid'], errors='coerce')
            self.log.info("Cleaned 'userid' column, converting non-numeric values to NULL.")
        
        df.to_sql(self.table, engine, if_exists='append', index=False)
        self.log.info(f"Successfully staged data to {self.table} table.")