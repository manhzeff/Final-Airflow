from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators.stage_postgres import StageToPostgresOperator
from operators.load_dimensions import LoadDimensionOperator
from operators.load_fact import LoadFactOperator
from operators.data_quality import DataQualityOperator

from helpers.sql_queries import SqlQueries

DATA_PATH = "/opt/airflow/config" 
SONG_DATA_PATH = f"{DATA_PATH}/song_data"
LOG_DATA_PATH = f"{DATA_PATH}/log_data"

default_args = {
    'owner': 'manhzeff',
    'start_date': datetime(2025, 7, 20),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('final_project_local_dag',
          default_args=default_args,
          description='Load and transform data in PostgreSQL with Airflow',
          schedule_interval='@hourly',
            max_active_runs=1,
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_postgres = StageToPostgresOperator(
    task_id='Stage_events',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="staging_events",
    data_path=LOG_DATA_PATH
)

stage_songs_to_postgres = StageToPostgresOperator(
    task_id='Stage_songs',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="staging_songs",
    data_path=SONG_DATA_PATH
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="songplays",
    sql_query=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="users",
    sql_query=SqlQueries.user_table_insert,
    truncate=True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="songs",
    sql_query=SqlQueries.song_table_insert,
    truncate=True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="artists",
    sql_query=SqlQueries.artist_table_insert,
    truncate=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    postgres_conn_id="postgres_default",
    table="time",
    sql_query=SqlQueries.time_table_insert,
    truncate=True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    postgres_conn_id="postgres_default",
    tables=["songplays", "users", "songs", "artists", "time"]
)

end_operator = DummyOperator(task_id='End_execution',  dag=dag)



start_operator >> [stage_events_to_postgres, stage_songs_to_postgres]



[stage_events_to_postgres, stage_songs_to_postgres] >> load_songplays_table



load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table]



[load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks



run_quality_checks >> end_operator