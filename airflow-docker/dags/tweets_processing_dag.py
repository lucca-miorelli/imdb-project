from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime
from get_counts_to_dataframe import *
from get_recent_tweets_to_dataframe import *

default_args = {

    "start_date" : datetime(2022,3,1),

    "schedule_interval" : '0 13 * * *'     # DEFINIR INTERVALO

    }

dag_variables = Variable.get("dag_variables_config", deserialize_json=True)
TWITTER_TOKEN = dag_variables['TWITTER_TOKEN']
RDS_USER = dag_variables['RDS_USER']
RDS_PASSWORD = dag_variables['RDS_PASSWORD']
RDS_HOST = dag_variables['RDS_HOST']
RDS_NAME = dag_variables['RDS_NAME']


with DAG(dag_id="tweets_processing_dag",
        default_args=default_args,
        catchup=False) as dag:

    # Define tasks/operators

    get_counts_per_movie = PythonOperator(
        task_id = 'get_counts_per_movie',
        python_callable = main_function_counts,
        op_args=[TWITTER_TOKEN, RDS_USER, RDS_PASSWORD, RDS_HOST, RDS_NAME]
    )

    get_recent_tweets_per_movie = PythonOperator(
        task_id = 'get_recent_tweets_per_movie',
        python_callable = main_function_tweets,
        op_args=[TWITTER_TOKEN, RDS_USER, RDS_PASSWORD, RDS_HOST, RDS_NAME]
    )

    get_counts_per_movie >> get_recent_tweets_per_movie