import tweepy
import pandas as pd
import configparser
from sqlalchemy import create_engine
from contextlib import contextmanager
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





def main_function_tweets(TWITTER_TOKEN, RDS_USER, RDS_PASSWORD, RDS_HOST, RDS_NAME):
    
    #credential = configparser.ConfigParser()
    #credential.read('credentials.conf')
    client = tweepy.Client(TWITTER_TOKEN)

    with create_db_engine(
        db_user=RDS_USER,
        db_password=RDS_PASSWORD,
        host=RDS_HOST,
        db_name=RDS_NAME
    ) as engine:

        df_imdb = read_data("SELECT * FROM imdb_kaggle", engine)
        df_tweets = pd.DataFrame(columns=['movie_id', 'movie', 'tweet_id', 'created_at'])

        for id, movie in enumerate(df_imdb.sort_values(by='imdb', ascending=False)['title'][0:25]):
            
            query = "\"{}\"".format(movie.replace(":",""))

            response = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=50)
            tweets = response.data
            
            tt_ids = [
                t.id for t in tweets
            ]

            created_at = [
                t.created_at for t in tweets
            ]

            movie_list = [movie] * len(tt_ids)

            movie_id_list = np.ones(len(tt_ids), dtype=int) * (id+1)

            df_temp = pd.DataFrame(list(zip(movie_id_list, movie_list, tt_ids, created_at)),
                                    columns=['movie_id', 'movie', 'tweet_id', 'created_at'])
            df_tweets = pd.concat([df_tweets, df_temp], axis=0)

        df_tweets['created_at'] = pd.to_datetime(df_tweets.created_at)
        df_tweets.astype({
            'movie': str,
            'movie_id': str,
            'tweet_id': str
        })

        df_tweets.to_sql(name='tweets_per_movie',
                if_exists='append',
                con=engine,
                index=False)




#main_function_tweets()