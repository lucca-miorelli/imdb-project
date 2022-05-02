# Libraries
import configparser
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Output, Input
import dash_bootstrap_components as dbc
from contextlib import contextmanager
from sqlalchemy import create_engine


# Credentials
credential = configparser.ConfigParser()
credential.read("credentials.conf")


# Constants
COLORS = dict(
    background  = "#151515",
    text        = "#eeeeee"
)
COLOR_PALETTE   = ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"]

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




def generate_datatable(table:str, nrows:int=10):

    query = f"SELECT * FROM {table} LIMIT {nrows}"
    
    with create_db_engine(**SQLALCHEMY_ENG) as engine:
        df = pd.read_sql_query(query, engine)
    
    return dash_table.DataTable(
        id='tb1',
        data=df.to_dict('records'), 
        columns=[{'name': col, 'id': col} for col in df.columns],
        style_data=dict(
            whiteSpace='normal',
            height='auto',
            # backgroundColor='#191919',
            textAlign='center',
            fontSize=10
        ),
        style_data_conditional=[{
            'if': dict(row_index='odd'),
            # 'backgroundColor':'#383838'
        }],
        style_header=dict(
            # backgroundColor='#131313',
            fontWeight='bold',
            textAlign='center'
        )
    )







# Dash

# app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], title='DE Mentorship - IMDB')
app = Dash(__name__, title='DE Mentorship - IMDB')


app.layout = html.Div(
    style=dict(
        marginLeft='5%',
        marginRight='5%'
    ),
    children=[
        html.H1(
            children='IMDB and Twitter dashboard',
            style=dict(
                textAlign='center'
            )
        ),
        html.Div(
            children='Group: Diego Jardim, Lucca Miorelli, Luiz Alves, Samuel Dieterich',
            style=dict(
                textAlign='center'
            )
        ),
        html.Div(
            style=dict(
                marginTop='20px',
                # marginLeft='5%',
                # marginRight='5%'
            ),
            children=[
                html.H2(
                    children='IMDB Kaggle dataset'
                ),
                generate_datatable(
                    table='imdb_kaggle', 
                    nrows=5
                )
            ]
        ),
        html.Div(
            style=dict(
                marginTop='20px'
            ),
            children=[
                html.H2(
                    children='IMDB Kaggle Stats'
                ),
                dcc.Dropdown(['genre1', 'genre2', 'genre3'], 'genre1', id='dropdown_gender'),
                dcc.Graph(id='gender_pie')
            ]
        )
    ]
)


@app.callback(
    Output('gender_pie', 'figure'),
    Input('dropdown_gender', 'value')
)
def pie_gender_update(genre_select):
    query = f"SELECT {genre_select} FROM imdb_kaggle"
    
    with create_db_engine(**SQLALCHEMY_ENG) as engine:
        df = pd.read_sql_query(query, engine)
    
    fig = px.pie(df, names=df[genre_select].unique(), values=df[genre_select].value_counts())

    # fig.update_layout(transition_duration=500)

    return fig






if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
