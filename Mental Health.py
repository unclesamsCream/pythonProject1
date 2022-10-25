'''
Author: Tao
Date: 2022-10-21 11:00:14
LastEditors: Tao
LastEditTime: 2022-10-25 16:18:23
Description:
Email: 202203580@post.au.dk
Copyright (c) 2022 by Tao Tang, All Rights Reserved.
'''
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from gc import callbacks
import ssl
from tkinter.ttk import Style
from turtle import shape

ssl._create_default_https_context = ssl._create_unverified_context

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json') as response:
    counties = json.load(response)

app = Dash(__name__)

# * Read data (page 0~5) from excel
df = []

df0 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=0)
df.append(df0)

df1 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=1)
df.append(df1)

df2 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=2)
df.append(df2)

df3 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=3)
df.append(df3)

df4 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=4)
df.append(df4)

df5 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=5)
df.append(df5)

#? *******************************************Layout Design Part*************************************************

# * Design the layout of the whole data visualization
app.layout = html.Div([
    # * Title: 'THe Worldwide Mental Health Depression Disorder Data Visualization'
    html.Div(
        html.H1(
            'THe Worldwide Mental Health Depression Disorder Data Visualization',
            style={'textAlign': 'center'}
        )
    ),

    # * Select a region
    html.Div([
        html.P(
            'Select a Region',
            # style={'textAlign' : 'center'}
        ),
        dcc.Dropdown(
            ['world', 'europe', 'asia', 'africa', 'north america', 'south america'],
            id='region_selection'
        )
    ]),

    html.Br(),

    # * Map
    dcc.Graph(id="graph_map"),

    html.Br(),
    
    # * Slider
    dcc.Slider(
        df[0]['Year'].min(),
        df[0]['Year'].max(),
        step=None,
        id='year_slider',
        value=df[0]['Year'].min(),
        marks={str(year): str(year) for year in df[0]['Year'].unique()}
    ),

    html.Br(),

    # * Line chart
    dcc.Graph(id='graph_line_chart')
])

#? *******************************************Interaction Part*************************************************

@app.callback(
    Output("graph_map", "figure"),
    Input("year_slider", "value"),
    Input("region_selection", "value")
)
def update_graph_map(year_value, region_value):
    # * Filter the data from the selected year
    df0Filtered = df[0][df[0]['Year'] == year_value]
    # * Update the colored map
    fig = px.choropleth(df0Filtered, locations='Code', color='Depression (%)',
                        color_continuous_scale='Viridis',
                        scope=region_value,
                        range_color=(0, 10),
                        hover_name='Entity',
                        labels={'Depression (%)': 'Depression rate'})
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')
    return fig

# * Define line_chart_creator
def line_chart_creator(dff, title):
    fig = px.scatter(dff, x='Year', y='Depression (%)')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.add_annotation(x=0, y=0, xanchor='left', yanchor='bottom',
                    xref='paper', yref='paper', showarrow=False, align='left',
                    text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig

# * Callback - Click data and update the line chart
@app.callback(
    Output('graph_line_chart', 'figure'),
    Input('graph_map', 'clickData')
)

def update_graph_line_chart(clickData):
    default_country = 'Denmark'
    default_df = df[0][df[0]['Entity'] == default_country]
    if clickData == None:
        return line_chart_creator(default_df, default_country)
    country_name = clickData['points'][0]['hovertext']
    dff = df[0][df[0]['Entity'] == country_name]
    return line_chart_creator(dff, country_name)

if __name__ == '__main__':
    app.run_server(debug=True)