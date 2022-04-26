# Libraries
import os
import pandas as pd
import numpy as np
import csv


# Constants
DATA_FILE       = os.path.join("data", "imdb_top_1000.csv")
RENAME_FILE     = os.path.join("helper", "imdb_kaggle_rename_cols.csv") 
PROCESSED_FILE  = os.path.join("data", "imdb_top_1000.parquet")


# Filter the columns to be loaded
all_columns = pd.read_csv(DATA_FILE, nrows=0).columns
use_cols    = np.setdiff1d(all_columns, ["Poster_Link"]) 


# Load dataset
df = pd.read_csv(DATA_FILE, usecols=use_cols)


# Rename dataframe
with open(RENAME_FILE) as file:
    rename_dict = dict(csv.reader(file))
df.rename(columns=rename_dict, inplace=True)


# Cleaning

## released_year: object -> int
df.released_year.replace({"PG": 1995}, inplace=True)              # Apollo 13
df.released_year = pd.to_numeric(df.released_year)

## runtime: remove 'min' -> int
df.runtime = df.runtime.apply(lambda x: int(x.split()[0]))

## genre: split
df.insert(loc=5, column="genre1", value='')
df.insert(loc=6, column="genre2", value='')
df.insert(loc=7, column="genre3", value='')
df[["genre1", "genre2", "genre3"]] = df.genre.str.split(",", 2, expand=True)
df.drop(columns="genre", inplace=True)

## meta_score: float -> int
df.meta_score = df.meta_score.astype("Int64")

## gross: remove commas -> int
df.gross = df.gross.apply(lambda x: str(x).replace(",",""))
df.gross.replace({"nan":None}, inplace=True)
df.gross = df.gross.astype("Int64")


# Save dataset
df.to_parquet(PROCESSED_FILE)


# Show a preview
print(df)