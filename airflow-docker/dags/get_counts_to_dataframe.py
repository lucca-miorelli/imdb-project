# Libraries
import configparser
from contextlib import contextmanager
import pandas as pd
from sqlalchemy import create_engine
import tweepy
import os
import numpy as np



@contextmanager
def create_db_engine(db_user:str, db_password:str, host:str, db_name:str):
    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{host}:5432/{db_name}', echo=False)
        yield engine
    finally:
        engine.dispose()



def read_data(query:str, engine):
    try:
        return pd.read_sql_query(query, engine)
    except:
        print("Could not return data from query.")



def main_function_counts():

    credential = configparser.ConfigParser()
    credential.read(os.path.join("credentials.conf"))
    client = tweepy.Client(credential['TWITTER']['TOKEN'])

    with create_db_engine(
        db_user=credential["RDS"]["USER"],
        db_password=credential["RDS"]["PASSWORD"],
        host=credential["RDS"]["HOST"],
        db_name=credential["RDS"]["NAME"]
    ) as engine:
        
        df_imdb = read_data("SELECT * FROM imdb_kaggle", engine)
        df_counts = pd.DataFrame(columns=['movie_id', 'movie', 'end','start', 'tweet_count'])


        for id, movie in enumerate(df_imdb.sort_values(by='imdb', ascending=False)['title'][0:25]):

            query = "\"{}\"".format(movie.replace(":",""))

            counts = client.get_recent_tweets_count(query=query, granularity='day')

            end_dates = [
                e['end'] for e in counts.data
            ]
            start_dates = [
                s['start'] for s in counts.data
            ]
            tt_counts = [
                tc['tweet_count'] for tc in counts.data
            ]
            movies_list = [movie] * len(end_dates)
            
            ids_list = np.ones(len(end_dates), dtype=int) * (id+1)

            df_temp = pd.DataFrame(list(zip(ids_list, movies_list, end_dates, start_dates, tt_counts)),
                                    columns=['movie_id', 'movie', 'end', 'start', 'tweet_count'])

            df_counts = pd.concat([df_counts, df_temp], axis=0)

        df_counts['end'] = pd.to_datetime(df_counts.end, utc=True)
        df_counts['start'] = pd.to_datetime(df_counts.start, utc=True)
        df_counts['tweet_count'] = pd.to_numeric(df_counts.tweet_count)

        df_counts.astype({
            'movie': str,
            'movie_id': str
        })

        df_counts.to_sql(name='count_tweets_per_movie',
                    if_exists='append',
                    con=engine,
                    index=False)



                    

        

#main_function_counts()