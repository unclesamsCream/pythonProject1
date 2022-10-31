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
import plotly.graph_objs as go
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json') as response:
    counties = json.load(response)

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = Dash(__name__,
        external_stylesheets=external_stylesheets)

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

gender_data = pd.read_csv('gender.csv')
age_data = pd.read_csv('age.csv')

# * My color scale
# colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1", "#85bcdb"]

# endpts = list(np.linspace(0, 8, len(colorscale)))

# * Design the layout of the whole data visualization
app.layout = html.Div([
    # * Title: 'THe Worldwide Mental Health Depression Disorder Data Visualization'
    html.Div(
        html.H1(
            'THe Worldwide Mental Health Depression Disorder Data Visualization',
            style={'textAlign': 'center'}
        )
    ),

    html.Div([
        html.H5(
            'Tao Tang, Haoyu Guo',
            style={'textAlign' : 'right'}
        )
    ]),

    # * Select a region
    html.Div([
        html.P(
            'Select a Region',
            # style={'textAlign' : 'center'}
        ),
        dcc.Dropdown(
            ['world', 'europe', 'asia', 'africa', 'north america', 'south america'],
            id='region_selection',
            style={'width' : '30%','float' : 'left'}
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
        marks={str(year): str(year) for year in df[0]['Year'].unique()},
    ),
    html.Br(),
    # * Line chart
    html.Div([
    dcc.Graph(id='graph_line_chart', style={'width' : '49%', 'height' : '450px', 'float' : 'left'}),
    dcc.Graph(id='graph_bar', style={'width' : '49%', 'height' : '450px', 'float' : 'right'}),
    dcc.Graph(id='graph_parallel', style={'width' : '49%', 'height' : '450px', 'float' : 'left'}),
    dcc.Graph(id='graph_scatter', style={'width' : '49%', 'height' : '450px', 'float' : 'right'})
    ])
])
@app.callback(
    Output("graph_parallel", "figure"),
    Input("year_slider", "value")

)
def get_show_parallel_c(year_value):
    data = age_data[age_data['Year'] == year_value]
    fig = px.parallel_coordinates(data,
      dimensions=['10-14 years old (%)',  '15-49 years old (%)',
                  '50-69 years old (%)','70+ years old (%)','Age-standardized (%)'],
    )
    return fig
@app.callback(
    Output("graph_scatter", "figure"),
    Input("year_slider", "value")
)

def get_show_scatter(year_value):
    data = gender_data[gender_data['Year'] == year_value]
    # print(data)
    fig = px.scatter(
        data,
        x="Prevalence in males (%)",
        y="Prevalence in females (%)",
        text= "Entity"
        # color="species",
        # size='petal_length',
        # hover_data=['petal_width']
    )
    fig.add_shape(type="line",
      x0=0, y0=0, x1=10, y1=10,
      line=dict(
          color="MediumPurple",
          width=4,
          dash="dot",
      )
    )
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.update_layout(
        xaxis=dict(
            dtick = 1,
            range=(0, 10),
        ),
        yaxis=dict(
            dtick=1,
            range=(0, 10),
        ),
    )
    fig.update_layout(newshape_drawdirection= "diagonal")
    return fig
@app.callback(
    Output("graph_bar", "figure"),
    Input("year_slider", "value")
)
# * Define the bar chart of sorted data
def get_show_bar(year_value):
    select_data = df[0][df[0]['Year'] == year_value]
    select_data.sort_values(by="Depression (%)", inplace=True, ascending=False)
    select_data = select_data[0:10]
    fig = px.bar(
        select_data,
        x = 'Entity',
        y = 'Depression (%)'
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

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
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
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
    # all_age = age_data[age_data['Entity'] == country_name]
    return line_chart_creator(dff, country_name)

if __name__ == '__main__':
    app.run_server(debug=True)