from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
import tweepy

from datetime import datetime
from get_counts_to_dataframe import *
from get_recent_tweets_to_dataframe import *
#import logging
#from logger import SetUpLogging

# Init Logger

#SetUpLogging().setup_logging()

def is_api_available_function():
    #logging.debug("---Opening twitter client ---")
    client = tweepy.Client(TWITTER_TOKEN) 
    try:
        response = client.get_user(username='joaopedroffn')
        for key, value in dict(response.data).items():
            print(key, ':', value)
    except tweepy.errors.TwitterServerError:
        raise Exception("TwitterServerError again...")

default_args = {

    "start_date" : datetime(2022,3,1),

    "schedule_interval" : '0 13 * * *'     # DEFINIR INTERVALO

    }

#logging.debug("--- Initializing DAG Variables ---")
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
    #logging.debug("--- Checking if Twitter API is available ---")
    is_api_available = PythonOperator(
        task_id='is_api_available',
        python_callable=is_api_available_function
    )

    #logging.debug("--- Getting counts per movie ---")
    get_counts_per_movie = PythonOperator(
        task_id = 'get_counts_per_movie',
        python_callable = main_function_counts,
        op_args=[TWITTER_TOKEN, RDS_USER, RDS_PASSWORD, RDS_HOST, RDS_NAME]
    )

    #logging.debug("--- Getting recent tweets per movie ---")
    get_recent_tweets_per_movie = PythonOperator(
        task_id = 'get_recent_tweets_per_movie',
        python_callable = main_function_tweets,
        op_args=[TWITTER_TOKEN, RDS_USER, RDS_PASSWORD, RDS_HOST, RDS_NAME]
    )

    is_api_available >> get_recent_tweets_per_movie >> get_counts_per_movie