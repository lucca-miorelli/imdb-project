# Libraries
import configparser
import os
from contextlib import contextmanager
import pandas as pd
from sqlalchemy import create_engine


# Helper function
@contextmanager
def create_db_engine(db_user:str, db_password:str, host:str, db_name:str):
    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{host}:5432/{db_name}', echo=False)
        yield engine
    finally:
        engine.dispose()


# Credentials
credential = configparser.ConfigParser()
credential.read("credentials.conf")


# Send dataframe to RDS
df = pd.read_parquet(os.path.join("data", "imdb_top_1000.parquet"))
with create_db_engine(
    db_user=credential["RDS"]["USER"],
    db_password=credential["RDS"]["PASSWORD"],
    host=credential["RDS"]["HOST"],
    db_name=credential["RDS"]["NAME"]
) as engine:
    df.to_sql(name="imdb_kaggle", schema="public", if_exists='append', index=False, con=engine)
