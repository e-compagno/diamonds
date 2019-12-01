# https://dash.plot.ly/getting-started
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import sqlalchemy as db
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import os

# Load MYSql connector 
SQL_USR, SQL_PSW= os.environ['SQL_USR'], os.environ['SQL_PSW']
mysql_str = 'mysql+mysqlconnector://'+SQL_USR+':'+SQL_PSW+'@localhost:3306/'
engine = db.create_engine(mysql_str+'Diamonds')

# Load data
df = pd.read_sql('SELECT * FROM physical;', engine).drop('id', axis=1)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Select category(number columns)
cat_columns = df.select_dtypes(exclude=np.number).columns.tolist()
num_columns = df.select_dtypes(include=np.number).columns.tolist()

# cut category
cut_cat_order = ['Ideal', 'Premium', 'Good', 'Very Good', 'Fair']
cut_dtype = pd.api.types.CategoricalDtype(categories=cut_cat_order,\
                                          ordered=True)
df['cut'] = df['cut'].astype(cut_dtype)
cut_dict=[]
for idx, label in enumerate(cut_cat_order):
    cut_dict.append({'label': label, 'value': str(idx)})

# color category
color_cat_order=['D', 'E', 'F', 'G', 'H', 'I', 'J']
color_dtype = pd.api.types.CategoricalDtype(categories=color_cat_order,\
                                            ordered=True)
df['color'] = df['color'].astype(color_dtype)
color_dict=[]
for idx, label in enumerate(color_cat_order):
    color_dict.append({'label': label, 'value': str(idx)})

# clarity category
clarity_cat_order = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'][::-1]
color_dtype = pd.api.types.CategoricalDtype(categories=clarity_cat_order,\
                                            ordered=True)
df['clarity'] = df['clarity'].astype(color_dtype)
clarity_dict=[]
for idx, label in enumerate(clarity_cat_order):
    clarity_dict.append({'label': label, 'value': str(idx)})

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div(children=[

html.Div(children=[
    # First application block
    # Summary block 
    html.H1(children='Diamond Dashboard',
        style={
            'textAlign': 'center'
        }),

    html.Div(
        children="""
        Diamond dashbord.
        """
    ),

    html.H4(children='Diamond dataset'),

    # Head table
    generate_table(df, max_rows=5),
    ]),

    # Second application block
    # Input values
    html.Div(children=[
        # Category selection
        html.Label('cut'),
        dcc.Dropdown(
            id='cut-dropdown',
            options=cut_dict,
            value=['cut_value']
        ),

        html.Label('colour'),
        dcc.Dropdown(
            id='color-dropdown',
            options=color_dict,
            value=['color_value']
        ),

        html.Label('clarity'),
        dcc.Dropdown(
            id='clarity-dropdown',
            options=clarity_dict,
            value=['clarity_value']
        ),

        html.Label('carat'),
        dcc.Input(
            id='carat-input',
            value='carat',
            type='text'
        ),

        html.Label('depth'),
        dcc.Input(
            id='depth-input',
            value='depth',
            type='text'
        ),

        html.Label('table'),
        dcc.Input(
            id='table-input',
            value='table',
            type='text'
        ),

        html.Label('x'),
        dcc.Input(
            id='x-input',
            value='x',
            type='text'
        ),

        html.Label('y'),
        dcc.Input(
            id='y-input',
            value='y',
            type='text'
        ),

        html.Label('z'),
        dcc.Input(
            id='z-input',
            value='z',
            type='text'
        ),

    # End Div     
    ],
    style={'columnCount': 2}
    )

])



if __name__ == '__main__':
    app.run_server(debug=True)