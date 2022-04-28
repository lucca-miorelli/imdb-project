create table counts_tweets_per_movie
(
    "movie_id"    text not null,
    "movie"       text not null,
    "end"       date not null,
    "start"       date not null,
    "tweet_count" int  not null
);
