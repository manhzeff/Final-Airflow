# operators/load_fact.py
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="postgres_default", 
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id 
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id) 
        self.log.info(f"Loading data into fact table {self.table}")
        postgres.run(f"INSERT INTO {self.table} {self.sql_query}")