from get_counts_to_dataframe import *
from get_recent_tweets_to_dataframe import *
import configparser
import os
#import logging
#from logger import SetUpLogging

# Init Logger

SetUpLogging().setup_logging()

credential = configparser.ConfigParser()
credential.read('..\..\credentials.conf')

print("Script started running...")
#logging.debug("--- Script started running ---")

main_function_counts(
    TWITTER_TOKEN=credential['TWITTER']['TOKEN'],
    RDS_USER=credential['RDS']['USER'],
    RDS_PASSWORD=credential['RDS']['PASSWORD'],
    RDS_HOST=credential['RDS']['HOST'],
    RDS_NAME=credential['RDS']['NAME']
)

print('Counts done!')
#logging.debug("--- Counts done! ---")

main_function_tweets(
    TWITTER_TOKEN=credential['TWITTER']['TOKEN'],
    RDS_USER=credential['RDS']['USER'],
    RDS_PASSWORD=credential['RDS']['PASSWORD'],
    RDS_HOST=credential['RDS']['HOST'],
    RDS_NAME=credential['RDS']['NAME']
)

print('Tweets done!')
#logging.debug("--- Tweets done! ---")
print('All done!')
#logging.debug("--- All done! ---")