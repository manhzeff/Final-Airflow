from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="postgres_default",
                 table="",
                 sql_query="",
                 truncate=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.sql_query = sql_query
        self.truncate = truncate

    def execute(self, context):
        postgre = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        if self.truncate:
            self.log.info(f"Truncating dimension table: {self.table}")
            postgre.run(f"TRUNCATE TABLE {self.table}")

        self.log.info(f"Loading data into dimension table {self.table}")
        postgre.run(f"INSERT INTO {self.table} {self.sql_query}")