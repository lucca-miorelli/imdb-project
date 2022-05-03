# Libraries
import configparser
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
from contextlib import contextmanager
from sqlalchemy import create_engine


# Credentials
credential = configparser.ConfigParser()
credential.read("credentials.conf")

HOST            = credential.get('RDS', 'HOST')
DATABASE        = credential.get('RDS', 'NAME')
USER            = credential.get('RDS', 'USER')
PASSWORD        = credential.get('RDS', 'PASSWORD')
SQLALCHEMY_ENG  = dict(db_user=USER, db_password=PASSWORD, host=HOST, db_name=DATABASE)

del credential


# Helper function
@contextmanager
def create_db_engine(db_user:str, db_password:str, host:str, db_name:str):
    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{host}:5432/{db_name}', echo=False)
        yield engine
    finally:
        engine.dispose()


# Get date_range
with create_db_engine(**SQLALCHEMY_ENG) as engine:
    query = "SELECT MIN(start), MAX(start) FROM count_tweets_per_movie"
    df = pd.read_sql_query(query, con=engine)
    date_range = df.to_dict('records')[0]


# Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], title='DE Mentorship - IMDb')

app.layout = html.Div(
    style=dict(
        marginLeft='5%',
        marginRight='5%',
        marginTop='20px',
        textAlign='center'
    ),
    children=[
        html.H1(children='IMDb and Twitter dashboard',),
        html.P(children='Group: Diego Jardim, Lucca Miorelli, Luiz Alves, Samuel Dieterich',),
        html.Div(
            style=dict(marginTop='20px'),
            children=[
                dcc.Graph(id='tweets_counts_graph'),
                dcc.DatePickerRange(
                    id='date_picker',
                    min_date_allowed=date_range['min'],
                    max_date_allowed=date_range['max'],
                    start_date=date_range['min'],
                    end_date=date_range['max'],
                )
            ]
        )
    ]
)


@app.callback(
    Output('tweets_counts_graph', 'figure'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date'),
)
def tweets_counts_graph_update(start_date=date_range['min'], end_date=date_range['max']):

    start_date = date_range['min'] if start_date is None else start_date
    
    query = f"""
    SELECT movie, start, tweet_count 
    FROM count_tweets_per_movie
    WHERE start BETWEEN '{start_date}' AND '{end_date}'
    """
    
    with create_db_engine(**SQLALCHEMY_ENG) as engine:
        df = pd.read_sql_query(query, engine)

    
    df = df.groupby(by=['movie', 'start']).mean()
    df.reset_index(inplace=True)


    fig = px.line(
        df, 
        x='start', 
        y='tweet_count', 
        color='movie',
        labels=dict(
            start='Date',
            tweet_count='Tweet count',
            movie='Movie'
        ),
        template='plotly_dark'
    )

    fig.update_traces(
        hovertemplate="%{y}<extra><b>%{fullData.name}</b></extra>"
    )

    fig.update_layout(
        title=dict(
            text='Tweet count (moving average) by movie',
            font_size=20
        ),
        transition_duration=500, 
        height=600,
        template='plotly_dark',
        paper_bgcolor='#060606',
        plot_bgcolor='#060606'
    )

    return fig



if __name__ == '__main__':

    app.run_server(
        debug=True, 
        dev_tools_hot_reload=True
    )
