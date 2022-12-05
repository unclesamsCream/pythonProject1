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
import dash
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


gender_data = pd.read_csv('gender.csv')
age_data = pd.read_csv('age.csv')
suicide_data = pd.read_csv('suicide.csv')
data_fusion = pd.read_csv('data_fusion.csv')
# * My color scale
# colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1", "#85bcdb"]

# endpts = list(np.linspace(0, 8, len(colorscale)))

# * Design the layout of the whole data visualization
colors = {
    'background': '#f2f2f2',
    'text': '#323232'
}

app.layout = \
    html.Div(
            style={'background-color': '#f2f2f2'},
            children = [
    # * Title: 'THe Worldwide Mental Health Depression Disorder Data Visualization'
    html.Br(),
    html.Div(
        html.H1(
            'THe Worldwide Depression Disorder Data Visualization',
            style={'padding': '2%','textAlign': 'center'}
        ),
        style={
            'background-color': 'white',
            # 'margin-top': '2%',
            # 'width' : '%',
            # 'height' : '200%',
            'margin-bottom': '1%',
            'margin-right':'3%',
            'margin-left' :'3%'
        }
    ),
    html.Div(
        [
            html.H5(
                'Select Regions',
                style={'padding': '2%','textAlign': 'center'}
            ),
            dcc.Checklist(
                id='region_choice',
                options=[
                    {'label': 'World', 'value': 'World'},
                    {'label': 'Asia', 'value': 'Asia'},
                    {'label': 'Europe', 'value': 'Europe'},
                    {'label': 'Africa', 'value': 'Africa'},
                    {'label': 'Oceania', 'value': 'Oceania'},
                    {'label': 'Americas', 'value': 'Americas'},
                ],
                value=['World'],
                style={
                    'padding': '1%',
                    'display': 'flex',
                    'justify-content': 'center'
                }
            ),
        ],
        style={
            'background-color': 'white',
            # 'margin-top': '2%',
            'height' : '100px',
            'width' : '23%',
            'margin-left': '3%',
            'float' : 'left',
            'padding': '0.5%',
            'margin-bottom': '1%',
        }
    ),
    html.Div(
        [
            html.H5(
                'Select Year',
                style={'padding': '0.8%','textAlign': 'center'}
            ),
            dcc.Slider(
                df[0]['Year'].min(),
                df[0]['Year'].max(),
                step=None,
                id='year_slider',
                value=df[0]['Year'].min(),
                marks={str(year): str(year) for year in df[0]['Year'].unique()},
            ),
        ],
        style={
            'background-color': 'white',
            'height' : '100px',
            'width' : '70%',
            'margin-right': '3%',
            'float' : 'right',
            'padding': '0.5%',
            'margin-bottom': '1%',
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),
    html.Div(
        [
            html.H3(
                'Top 15',
                id='title_bar',
                style={'padding': '2%', 'textAlign': 'center'}
                # style={'margin-right': '100px', 'float': 'right'}
            ),
            dcc.RadioItems(
                id='mode_switch',
                options=['Top', 'Last'],
                value='Top',
                style={
                    'display': 'flex',
                    'justify-content': 'center'
                }
            ),
            dcc.Graph(id='graph_bar',
                      # style={'width': '70%', 'height': '600px'}
                      ),
        ],
        style={
            'background-color': 'white',
            'height': '500px',
            'width': '27.5%',
            'margin-left': '3%',
            'float': 'left',
            'margin-bottom': '1%',
            'padding': '1%'
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),
    html.Div(
        [
            html.H3(
                'Global share of the population with depression in all age groups',
                id='title_parallel',
                style={'padding': '2%', 'text-align': 'center'}
            ),
            dcc.Graph(id='graph_parallel',
                      # style={'width' : '100%', 'height' : '550px', 'margin' : '0 auto', 'overflow' : 'hidden'}
                      ),
        ],
        style={
            'background-color': 'white',
            'height': '500px',
            'width': '65.5%',
            'margin-right': '3%',
            'float': 'right',
            'overflow': 'hidden',
            'margin-bottom': '1%',
            'padding': '1%'
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),
    html.Div(
        [
            html.H3(
                'The rate of change in depression rate VS. The rate of change in suicide rate',
                id='title_scatter_gender',
                style={'padding': '2%','textAlign': 'center'}
            ),
            dcc.Graph(id='graph_suicide_depression_scatter',
                style={
                  # 'height': '500px',
                  'margin': 'auto'
                }
            ),
        ],
        style={
            'background-color': 'white',
            'height' : '500px',
            'width': '46.5%',
            'margin-left': '3%',
            'float': 'left',
            'overflow': 'hidden',
            'margin-bottom': '1%',
            # 'padding': '1%'
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),
    html.Div(
        [
            html.H3(
                'Global prevalence of depression in males and females',
                id='title_scatter_suicide',
                style={'padding': '2%','textAlign': 'center'}
            ),
            dcc.Graph(id='graph_gender_scatter',
                style={
                    # 'height' : '500px',
                    'margin': 'auto'
                }
            ),
        ],
        style={
            'background-color': 'white',
            'height' : '500px',
            'width': '46.5%',
            'margin-right': '3%',
            'float': 'right',
            'overflow': 'hidden',
            'margin-bottom': '1%',
            # 'padding': '1%'
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),

    html.Div(
        [
            html.H3(
                'Share of the population with depression',
                id='title_map_new',
                style={'padding': '0.8%','textAlign': 'center'}
            ),
            dcc.Graph(id="graph_map",
                      # style={'width': '69%', 'height': '450px', 'float': 'left', 'margin-left': '55px'}
            ),
            # html.Div(
            #     [
            #         html.P(
            #             'Select a Region',
            #             style={'margin-left': '30px'}
            #         ),
            #         dcc.Dropdown(
            #             ['world', 'europe', 'asia', 'africa', 'north america', 'south america'],
            #             id='region_selection',
            #             # style={'width' : '30%', 'height' : '500px', 'float' : 'left'}
            #             # style={'width': '30%', 'margin-left': '15px'}
            #         )
            #     ]
            # ),
        ],
        style={
            'background-color': 'white',
            'height': '550px',
            'width': '50%',
            'margin-left': '3%',
            'float': 'left',
            'overflow': 'hidden',
            'margin-bottom': '1%',
            'padding': '1%'
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),
    html.Div(
        [
        dcc.Tabs(
            id='details_selection',
            value='tab-1',
            children=
            [
            dcc.Tab(
                value='tab-1',
                label='Prevalence of Depression in Age Standardized & All ages'
            ),
            dcc.Tab(
                value='tab-2',
                label='Prevalence of Depression in 4 Age Groups'
            ),
            dcc.Tab(
                value='tab-3',
                label='Prevalence of Depression in Males and Females'
            ),
            dcc.Tab(
                value='tab-4',
                label='Suicide rate VS. Depression rate'
            ),
            ]
        ),
        html.H3(
            'Prevalence of Depression in Age Standardized & All ages',
            id='title_details_graph',
            style={'text-align': 'center'}
        ),
        dcc.Graph(
            id='details_line_charts',
            # style={'width': '70%', 'margin': '0 auto'}
        ),
        ],
        style={
            'background-color': 'white',
            'height' : '550px',
            'width': '43%',
            'margin-right': '3%',
            'float': 'right',
            'overflow': 'hidden',
            'margin-bottom': '1%',
            # 'padding': '1%'
            # 'margin': '0 auto', 'overflow': 'hidden'
        }
    ),

# html.Div([
    #     html.H5(
    #         'Tao Tang, Haoyu Guo',
    #         style={'textAlign' : 'right', 'margin-right' : '55px'}
    #     )
    # ]),

    # * Select a region


    # * Line chart
    # html.Div([
    # dcc.Tabs(
    #     [
    #         #* Overview
    #         dcc.Tab(
    #             [
    #                 html.Br(),
    #                 html.Br(),
    #                 html.Br(),
    #                 #*Titles
    #                 html.Div([
    #                     html.H3(
    #                     'The rate of change in depression rate VS. The rate of change in suicide rate',
    #                     id='title_scatter_suicide',
    #                 style={'margin-left' : '100px', 'float' : 'left'}),
    #                     html.H3(
    #                     'Global prevalence of depression in males and females',
    #                     id='title_scatter_gender',
    #                 style={'margin-right' : '140px','float' : 'right'})]
    #                 ,style={'overflow' : 'hidden'}),
    #
    #                 #* Scatterplots
    #                 #dcc.Graph(id='graph_parallel', style={'width' : '50%', 'height' : '450px', 'float' : 'left'}),
    #                 dcc.Graph(id='graph_gender_scatter', style={'width' : '50%', 'height' : '450px', 'float' : 'right'}),
    #                 dcc.Graph(id='graph_suicide_depression_scatter',style={'width' : '50%', 'height' : '450px', 'float' : 'left'}),
    #                 html.Br(),
    #                 #* Parallel coordinates
    #                 html.Div([
    #                     html.H3(
    #                         'Global share of the population with depression in all age groups',
    #                         id='title_parallel',
    #                         style={'text-align' : 'center'}),
    #                     dcc.Graph(id='graph_parallel', style={'width' : '100%', 'height' : '550px', 'margin' : '0 auto', 'overflow' : 'hidden'}),
    #                     ]),
    #             ],
    #             label='Overview of global depression situation'
    #         ),
    #
            #* Details
            # dcc.Tab(
            #     [
            #         #html.Br(),
            #         #html.P('graph_line_chart'),
            #         dcc.Graph(id='graph_line_chart', style={'width' : '70%', 'margin' : '0 auto'})
            #     ],
            #     label='Prevalence of Depression in all ages'
            # ),
            # dcc.Tab(
            #     [
            #         #html.Br(),
            #         #html.P('graph_4age_line_chart'),
            #         dcc.Graph(id='graph_4age_line_chart', style={'width' : '70%', 'margin' : '0 auto'}),
            #     ],
            #     label='Prevalence of Depression in 4 age groups'
            # ),
            # dcc.Tab(
            #     [
            #         #html.Br(),
            #         #html.P('graph_gender_line'),
            #         dcc.Graph(id='graph_gender_line', style={'width' : '70%', 'margin' : '0 auto'}),
            #     ],
            #     label='Prevalence of Depression in males and females'
            # ),
            # dcc.Tab(
            #     [
            #         #html.Br(),
            #         #html.P('graph_suicide_line'),
            #         dcc.Graph(id='graph_suicide_line', style={'width' : '70%', 'margin' : '0 auto'}),
            #     ],
            #     label='Suicide rate VS. Depression rate'
            # ),
    #     ], style={'width' : '90%', 'margin' : '0 auto'}
    # )], style={'overflow' : 'hidden'}),
    #
    # dcc.RangeSlider(
    #     id='year-range-slider',
    #     min=1990, max=2017, step=1,
    #     marks={0: '0', 2.5: '2.5'},
    #     value=[1990, 2017]
    # ),
    # dcc.Graph(id='graph_suicide_depression_scatter')
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),


])



def group_depression(x):
    if x < 1:
        return '< 1%'
    elif x < 2:
        return '1% ~ 2%'
    elif x < 3:
        return '2% ~ 3%'
    elif x < 4:
        return '3% ~ 4%'
    elif x < 5:
        return '4% ~ 5%'
    elif x < 6:
        return '5% ~ 6%'
    elif x < 7:
        return '6% ~ 7%'
    elif x < 8:
        return '7% ~ 8%'

@app.callback(
    Output("title_details_graph", "children"),
    Input("details_selection", "value")
)

def update_title_details(details_selection):
    if details_selection == 'tab-1':
        return 'Prevalence of Depression in Age Standardized & All ages'
    elif  details_selection == 'tab-2':
        return 'Prevalence of Depression in 4 Age Groups'
    elif details_selection == 'tab-3':
        return 'Prevalence of Depression in Males and Females'
    elif details_selection == 'tab-4':
        return 'Suicide rate VS. Depression rate'

@app.callback(
    Output("graph_bar", "figure"),
    [Input("year_slider", "value"),
    Input("mode_switch", "value")]
)
# * Define the bar chart of sorted data
def get_show_bar(year_value, display_mode):
    select_data = df[0][df[0]['Year'] == year_value]
    select_data.sort_values(by="Depression (%)", inplace=True, ascending=False)
    if(display_mode == 'Top'):
        select_data = select_data[0:15]
        select_data = select_data[::-1]
    else:
        select_data = select_data[::-1]
        select_data = select_data[:15]
        #select_data = select_data[::-1]
    #     select_data = select_data[0:15]
    #     select_data = select_data[::-1]

    fig = px.bar(
        select_data,
        y = 'Entity',
        x = 'Depression (%)',
        orientation='h',
        #color= 'Depression (%)',
        text_auto='.2f'
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    #fig.update_traces(textposition="outside")
    fig.update_traces(marker_color='#205EA8')
    return fig


#    ['world', 'europe', 'asia', 'africa', 'north america', 'south america'],
@app.callback(
    Output("graph_map", "figure"),
    Input("year_slider", "value"),
    Input("region_choice", "value")
)

def update_graph_map(year_value, region_value):
    #print(df[0]['Depression (%)'][0])
    #df[0].sort_values(by='Depression (%)', ascending=False)
    df[0]['Depression Rate'] = df[0]['Depression (%)'].apply(group_depression)
    colors = px.colors.qualitative.Set2
    # * Filter the data from the selected year
    df0Filtered = df[0][df[0]['Year'] == year_value]
    # * Update the colored map
    if not region_value or 'World' in region_value:
        region = 'world'
    else:
        if len(region_value) > 1:
            region = 'world'
        else:
            if region_value[0] == 'Asia':
                region = 'asia'
            elif region_value[0] == 'Europe':
                region = 'europe'
            elif region_value[0] == 'Africa':
                region = 'africa'
            else:
                region = 'world'
    fig = px.choropleth(df0Filtered, locations='Code', color='Depression Rate',
                        #color_continuous_scale='Viridis',
                        scope=region,
                        #color_discrete_sequence=px.colors.sequential.Greens,
                        color_discrete_sequence= ['#FFFFD8', '#ECF8B1', '#C9E9B4', '#7FCDBC', '#41B8C3', '#1D90C1', '#205EA8', '#0C2C85'],
                        #color_discrete_sequence=colors,
                        category_orders={'Depression Rate':['< 1%', '1% ~ 2%', '2% ~ 3%','3% ~ 4%', '4% ~ 5%', '5% ~ 6%', '6% ~ 7%', '7% ~ 8%']},
                        #range_color=(0, 10),
                        hover_name='Entity',
                        #labels={'Depression (%)': 'Depression rate'},
                        hover_data={'Year': True,
                                    'Depression (%)': ':.3f',
                                    'Depression Rate': False,
                                    'Code': False})
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')
    fig.update_layout(legend_traceorder="reversed")
    #fig.update_layout(legend_x=1.03, legend_y=1.11)
    #title = 'Share of the population with depression, ' + str(year_value)
    return fig

@app.callback(
    Output("title_bar", "children"),
    [
        Input("year_slider", "value"),
        Input('mode_switch', 'value')
    ]
)

def update_title_bar(year_value, mode_switch):
    title = 'Global ' + str(mode_switch)+ ' 15, ' + str(year_value)
    return title


@app.callback(
    Output("title_parallel", "children"),
    Input("year_slider", "value"),
)

def update_title_parallel(year_value):
    title = 'Global share of the population with depression in all age groups, ' + str(year_value)
    return title

@app.callback(
    Output("title_scatter_gender", "children"),
    Input("year_slider", "value"),
)

def update_title_scatter_gender(year_value):
    title = 'Global prevalence of depression in males and females, ' + str(year_value)
    return title

@app.callback(
    Output("title_map_new", "children"),
    Input("year_slider", "value"),
)

def update_title_map(year_value):
    title = 'Share of the population with depression, ' + str(year_value)
    return title

def update_graph_line_chart(clickData):
    default_country = 'Denmark'
    default_df = df[0][df[0]['Entity'] == default_country]
    default_all_age = age_data[age_data['Entity'] == default_country]
    # print(default_all_age)
    if clickData == None:
        return line_chart_creator(default_df,default_all_age, default_country)
    country_name = clickData['points'][0]['hovertext']
    dff = df[0][df[0]['Entity'] == country_name]
    all_age = age_data[age_data['Entity'] == country_name]
    # print(all_age)
    return line_chart_creator(dff,all_age, country_name)
# * Define line_chart_creator
def line_chart_creator(dff, all_age, country_title):
    fig = go.Figure()
    # print(list(dff['Year']))
    # print(list(dff['Depression (%)']))
    fig.add_trace(go.Scatter(x=dff['Year'], y=dff['Depression (%)'],
                             mode = 'lines+markers',
                             name = 'Age Standardized (%)'
                             ))
    fig.add_trace(go.Scatter(x=all_age['Year'], y=all_age['All ages (%)'],
                             mode = 'lines+markers',
                             name = 'All ages (%)'
                             ))
    # fig = px.scatter(dff, x='Year', y='Depression (%)')
    # fig.update_traces(mode='lines+markers')
    # fig.update_trace(dff, x='Year', y='Depression(%)')
    # fig.update_xaxes(showgrid=False)
    fig.add_annotation(x=0, y=0, xanchor='left', yanchor='bottom',
                    xref='paper', yref='paper', showarrow=False, align='left',
                    text=country_title)
    fig.update_layout(hovermode='x unified')

    fig.update_layout(template="simple_white")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig

# @app.callback(
#     Output('graph_4age_line_chart', 'figure'),
#     Input('graph_map', 'clickData')
# )
def update_graph_4age(clickData):
    default_country = 'Denmark'
    default_age_data = age_data[age_data['Entity'] == default_country]
    # print(default_age_data)
    if clickData == None:
        return age_chart_creator(default_age_data, default_country)
    country_name = clickData['points'][0]['hovertext']
    dff = age_data[age_data['Entity'] == country_name]
    # print(dff)
    return age_chart_creator(dff, country_name)

def age_chart_creator(age_data, country_title):
    fig = go.Figure()
    # print(list(dff['Year']))
    # print(list(dff['Depression (%)']))
    fig.add_trace(go.Scatter(x=age_data['Year'], y=age_data['10-14 years old (%)'],
                             mode='lines+markers',
                             name='10-14 years old (%)'
                             ))
    fig.add_trace(go.Scatter(x=age_data['Year'], y=age_data['15-49 years old (%)'],
                             mode='lines+markers',
                             name='15-49 years old (%)'
                             ))
    fig.add_trace(go.Scatter(x=age_data['Year'], y=age_data['50-69 years old (%)'],
                             mode='lines+markers',
                             name='50-69 years old (%)'
                             ))
    fig.add_trace(go.Scatter(x=age_data['Year'], y=age_data['70+ years old (%)'],
                             mode='lines+markers',
                             name='70+ years old (%)'
                             ))
    fig.add_annotation(x=0, y=0, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=country_title)
    fig.add_annotation(x=0, y=0, xanchor='left', yanchor='bottom',
                    xref='paper', yref='paper', showarrow=False, align='left',
                    text=country_title)
    fig.update_layout(hovermode='x unified')
    fig.update_layout(template="simple_white")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    # fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# @app.callback(
#     Output('graph_gender_line', 'figure'),
#     Input('graph_map', 'clickData')
# )
def update_graph_gender_line(clickData):
    default_country = 'Denmark'
    default_gender_data = gender_data[gender_data['Entity'] == default_country]
    default_all_age = age_data[age_data['Entity'] == default_country]
    # print(default_age_data)
    if clickData == None:
        return gender_line_creator(default_all_age, default_gender_data, default_country)
    country_name = clickData['points'][0]['hovertext']
    default_gender_data = gender_data[gender_data['Entity'] == country_name]
    default_all_age = age_data[age_data['Entity'] == country_name]
    return gender_line_creator(default_all_age, default_gender_data, country_name)

def gender_line_creator(all_age_data, gender_data, country_title):
    fig = go.Figure()
    # print(list(dff['Year']))
    # print(list(dff['Depression (%)']))
    fig.add_trace(go.Scatter(x=gender_data['Year'], y=gender_data['Prevalence in males (%)'],
                             mode='lines+markers',
                             name='Prevalence in males (%)'
                             ))
    fig.add_trace(go.Scatter(x=all_age_data['Year'], y=all_age_data['Age-standardized (%)'],
                             mode='lines+markers',
                             name='Both sexes'
                             ))
    fig.add_trace(go.Scatter(x=gender_data['Year'], y=gender_data['Prevalence in females (%)'],
                             mode='lines+markers',
                             name='Prevalence in females (%)'
                             ))
    fig.add_annotation(x=0, y=0, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=country_title)
    fig.update_layout(hovermode='x unified')
    fig.update_layout(template="simple_white")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    # fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# @app.callback(
#     Output('graph_suicide_line', 'figure'),
#     Input('graph_map', 'clickData')
# )
def update_graph_suicide_line(clickData):
    default_country = 'Denmark'
    default_suicide_data = suicide_data[suicide_data['Entity'] == default_country]
    default_all_age = age_data[age_data['Entity'] == default_country]
    # print(default_age_data)
    if clickData == None:
        return suicide_line_creator(default_all_age, default_suicide_data, default_country)
    country_name = clickData['points'][0]['hovertext']
    default_suicide_data = suicide_data[suicide_data['Entity'] == country_name]
    default_all_age = age_data[age_data['Entity'] == country_name]
    return suicide_line_creator(default_all_age, default_suicide_data, country_name)

def suicide_line_creator(all_age_data, suicide_data, country_title):
    fig = go.Figure()
    # print(list(dff['Year']))
    # print(list(dff['Depression (%)']))
    fig.add_trace(go.Scatter(x=suicide_data['Year'], y=suicide_data['Suicide rate (deaths per 100,000 individuals)'],
                             mode='lines+markers',
                             name='Suicide rate (deaths per 100,000 individuals)',
                             marker=dict(
                                 color="#1f77b4"
                             ),
                             ))
    fig.add_trace(go.Scatter(x=all_age_data['Year'], y=all_age_data['Age-standardized (%)']*1000,
                             yaxis="y2",
                             mode='lines+markers',
                             name='Depressive disorder rates (number suffering per 100,000)',
                             marker = dict(
                                color="#ff7f0e"
                             ),
                             ))
    fig.add_annotation(x=0, y=0, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=country_title)
    fig.update_layout(hovermode='x unified')
    fig.update_layout(template="simple_white")
    fig.update_layout(
        yaxis=dict(
            title="Suicide rate (deaths per 100,000 individuals)",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),

        yaxis2=dict(
            title="Depressive disorder rates (number suffering per 100,000)",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="x",
            overlaying="y",
            side="right"
        ),
    )
    # fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(showlegend=False)
    return fig

# def get_show_suicide_x_depress(slider_range):
#     # df = px.data.iris() # replace with your own data source
#     old_year, last_year = slider_range
#     # print(old_year)
#     # print(last_year)
#     old_suicide = suicide_data[suicide_data['Year'] == old_year]
#     last_suicide = suicide_data[suicide_data['Year'] == last_year]
#     old_depression = age_data[age_data['Year'] == old_year]
#     last_depression = age_data[age_data['Year'] == last_year]
#     suicide_change = pd.DataFrame()
#     for old_row in old_suicide.iterrows():
#         # print(old_row['Entity'])
#         for new_row in last_suicide.iterrows():
#             # print(new_row['Entity'])
#             # print(type(new_row['Entity']))
#             # print(type(old_row['Entity']))
#             if old_row[1]['Entity'] == new_row[1]['Entity']:
#                 change = new_row[1]['Suicide rate (deaths per 100,000 individuals)'] - old_row[1]['Suicide rate (deaths per 100,000 individuals)']
#                 suicide_change = suicide_change.append({"Entity": old_row[1]['Entity'], "suicide_change_rate": change},ignore_index=True)
#     # print("----------",suicide_change)
#     depression_change = pd.DataFrame()
#     for old_row in old_depression.iterrows():
#         for new_row in last_depression.iterrows():
#             if old_row[1]['Entity'] == new_row[1]['Entity']:
#                 change = (new_row[1]['Age-standardized (%)'] - old_row[1]['Age-standardized (%)'])*1000
#                 depression_change = depression_change.append({"Entity": old_row[1]['Entity'],"depression_change_rate" : change},ignore_index=True)
#     # print(depression_change)
#     df = pd.merge(suicide_change, depression_change, on=['Entity'])

#     fig = px.scatter(df, x='suicide_change_rate', y='depression_change_rate',hover_name='Entity')
#     fig.update_yaxes(range=[-850,850], zeroline= True,zerolinewidth=2, zerolinecolor='black')
#     fig.update_xaxes(range=[-50,50], zeroline= True,zerolinewidth=2, zerolinecolor='black')
#     fig.update_layout(template="simple_white")
#     fig.update_traces(marker_color='#205EA8')
#     return fig

# * Callback - Click data and update the line chart
@app.callback(
    Output('details_line_charts', 'figure'),
    [
        Input('graph_map', 'clickData'),
        Input('details_selection', 'value')
    ]
)
# 'Prevalence of Depression in all ages',
# 'Prevalence of Depression in 4 age groups',
# 'Prevalence of Depression in males and females',
# 'Suicide VS Depression'
def update_details_graph(clickData, details_selection):
    if details_selection == 'tab-1':
        return update_graph_line_chart(clickData)
    elif details_selection == 'tab-2':
        return update_graph_4age(clickData)
    elif details_selection == 'tab-3':
        return update_graph_gender_line(clickData)
    elif details_selection == 'tab-4':
        return update_graph_suicide_line(clickData)
    else:
        return update_graph_line_chart(clickData)

@app.callback(
    Output("graph_parallel", "figure"),
    Input("year_slider", "value"),
    Input('region_choice', 'value'),
)
def get_show_parallel_c(year_value, region_value):
    age = age_data[age_data['Year'] == year_value]
    data = pd.DataFrame()
    # print(region_value)
    if not region_value or 'World' in region_value:
        data = age
    else:
        data = age.loc[age['region'] == region_value[0]]
        for index in range(1,len(region_value)):
            temp = age.loc[age['region'] == region_value[index]]
            # pd.set_option('display.max_columns', None)
            # print("===========",temp)
            data = pd.concat([data,temp])
    data['region_id'] = data['region'].map({'Asia': 0.9, 'Europe': 0.7, 'Africa': 0.5,'Oceania':0.3,'Americas':0.1})
    fig = px.parallel_coordinates(
        data,
        dimensions=['10-14 years old (%)',  '15-49 years old (%)',
                  '50-69 years old (%)','70+ years old (%)','Age-standardized (%)'],
        color='region_id',
        range_color=[0.0, 1.0],
        color_continuous_scale=[
            (0.0, "#faa25a"), (0.2, "#faa25a"),
            (0.2, "#b05dfb"), (0.4, "#b05dfb"),
            (0.4, "#1dcd95"), (0.6, "#1dcd95"),
            (0.6, "#ea563c"), (0.8, "#ea563c"),
            (0.8, "#7169fb"), (1.0, "#7169fb"),
        ]
    )
        # showscale=True,
    fig.update_layout(coloraxis_colorbar=dict(
        title="Continent",
        tickvals=[0.9, 0.7, 0.5, 0.3, 0.1],
        ticktext=["Asia",'Europe','Africa','Americas','Oceania' ],
        lenmode="pixels", len=200,
    ))
    # data['region_id'] = data['region'].map({'Asia': 1, 'Europe': 2, 'Africa': 3,'Oceania':4,'Americas':5})
    # fig = go.Figure(data=
    #     go.Parcoords(
    #         line=dict(color=data['region_id'],
    #             color_continuous_scale=[
    #             (1, "#7169fb"),
    #             (2, "#ea563c"),
    #             (3, "#1dcd95"),
    #             (4, "#b05dfb"),
    #             (5, "#faa25a"),],
    #         showscale = False),
    #         dimensions=list([
    #             dict(label='10-14 years old (%)', values=data['10-14 years old (%)']),
    #             dict(label='15-49 years old (%)', values=data['15-49 years old (%)']),
    #             dict(label='50-69 years old (%)', values=data['50-69 years old (%)']),
    #             dict(label='70+ years old (%)', values=data['70+ years old (%)']),
    #             dict(label='Age-standardized (%)', values=data['Age-standardized (%)'])
    #         ])
    #     )
    # )
    # fig.update_layout(showlegend=False, paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')
    # fig.update_layout(
    #     plot_bgcolor='white',
    #     paper_bgcolor='lightgray'
    # )
    #fig.update_traces(marker=dict(color='#205EA8'))
    return fig
@app.callback(
    Output("graph_suicide_depression_scatter", "figure"),
    # Output("graph_gender_scatter", "figure"),
    Input("year_slider", "value"),
    Input('region_choice', 'value'),
    # Input('graph_suicide_depression_scatter', 'selectedData'),
    # Input('graph_gender_scatter', 'selectedData'),
)
# def callback(selected_year,selection1, selection2):
#     # print("11111",selection1)
#     # print("22222",selection2)
#
#     # suicide = suicide_data[suicide_data['Year'] == selected_year]
#     # gender = gender_data[gender_data['Year'] == selected_year]
#     data =  data_fusion[data_fusion['Year'] == selected_year]
#     selectedpoints = data.index
#     for selected_data in [selection1, selection2]:
#         if selected_data and selected_data['points']:
#             selectedpoints = np.intersect1d(selectedpoints, [p['customdata'] for p in selected_data['points']])
#     print(selectedpoints)
#     return [get_show_suicide_x_depress(selectedpoints),
#             get_gender_scatter(selectedpoints)]
def get_show_suicide_x_depress(year_value, region_value):
    sucide = data_fusion.loc[data_fusion['Year'] == year_value]
    data = pd.DataFrame()
    # print(region_value)
    if not region_value or 'World' in region_value:
        data = sucide
    else:
        data = sucide.loc[sucide['region'] == region_value[0]]
        for index in range(1,len(region_value)):
            temp = sucide.loc[sucide['region'] == region_value[index]]
            # pd.set_option('display.max_columns', None)
            # print("===========",temp)
            data = pd.concat([data,temp])
    # print(data)
    # selectedpoints = suicide.Entity
    # for selected_data in [selection1, selection2]:
    #     if selected_data and selected_data['points']:
    #         selectedpoints = np.intersect1d(selectedpoints, [p['hovertext'] for p in selected_data['points']])
    # print(selectedpoints)
    fig = px.scatter(data,
        x = 'Depressive disorder rates (number suffering per 100,000)',
        y = 'Suicide rate (deaths per 100,000 individuals)',
        color='region',
        color_discrete_map={
            "Asia": "#7169fb",
            "Europe": "#ea563c",
            "Africa": "#1dcd95",
            "Oceania": "#b05dfb",
            "Americas": "#faa25a",
            },
        hover_name='Entity')
    # fig.update_traces(selectedpoints=selectedpoints,
    #                   customdata=suicide.Entity,
    #                   mode='markers+text', marker={'color': 'rgba(0, 116, 217, 0.7)', 'size': 20},
    #                   unselected={'marker': {'opacity': 0.3}, 'textfont': {'color': 'rgba(0, 0, 0, 0)'}})
    #
    # fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5}, dragmode='select', hovermode=False)

    # fig.update_traces(selectedpoints=selectedpoints,
    #                   customdata=data_fusion.index)
    fig.update_layout(template="simple_white")
    # fig.update_traces(marker=dict(color='#205EA8'))

    return fig
@app.callback(
    # Output("graph_suicide_depression_scatter", "figure"),
    Output("graph_gender_scatter", "figure"),
    Input("year_slider", "value"),
    Input('region_choice', 'value'),
    # Input('graph_suicide_depression_scatter', 'selectedData'),
    # Input('graph_gender_scatter', 'selectedData'),
)
def get_gender_scatter(year_value,region_value):
    gender = data_fusion.loc[data_fusion['Year'] == year_value]
    data = pd.DataFrame()
    # print(region_value)
    if not region_value or 'World' in region_value:
        data = gender
    else:
        data = gender.loc[gender['region'] == region_value[0]]
        for index in range(1,len(region_value)):
            temp = gender.loc[gender['region'] == region_value[index]]
            # pd.set_option('display.max_columns', None)
            # print("===========",temp)
            data = pd.concat([data,temp])
    # selectedpoints = data.Entity
    # for selected_data in [selection1, selection2]:
    #     if selected_data and selected_data['points']:
    #         selectedpoints = np.intersect1d(selectedpoints, [p['hovertext'] for p in selected_data['points']])
    # print(data)
    fig = px.scatter(
        data,
        x="Prevalence in males (%)",
        y="Prevalence in females (%)",
        color='region',
        color_discrete_map={
            "Asia": "#7169fb",
            "Europe": "#ea563c",
            "Africa": "#1dcd95",
            "Oceania": "#b05dfb",
            "Americas": "#faa25a",
        },
        hover_name= "Entity"
        #text= "Entity"
        # color="species",
        # size='petal_length',
        # hover_data=['petal_width']
    )
    # fig.update_traces(selectedpoints=selectedpoints,
    #                   customdata=data_fusion.index)
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
            range=(0, 9),
        ),
        yaxis=dict(
            dtick=1,
            range=(0, 9),
        ),
    )
    fig.update_layout(newshape_drawdirection= "diagonal")
    fig.update_layout(template="simple_white")
    # fig.update_traces(marker=dict(color='#205EA8'))
    return fig

# @app.callback(
#     Output("graph_parallel", "figure"),
#     Output("graph_gender_scatter", "figure"),
#     #Output("graph_suicide_depression_scatter", "figure"),
#     [
#         Input("year_slider", "value"),
#         Input("graph_parallel", "selectedData"),
#         Input("graph_gender_scatter", "selectedData"),
#         #Input("graph_suicide_depression_scatter", "selectedData")
#     ]
# )

# def cross_filtering(selected_year, selection1, selection2):
#     if selection1 == None and selection2 == None:
#         selected_data = None
#     elif selection1 != None:
#         selected_data = selection1
#     elif selection2 != None:
#         selected_data = selection2
#     return [get_show_parallel_c(selected_year, selected_data),
#             get_show_scatter(selected_year, selected_data)]

if __name__ == '__main__':
    app.run_server(debug=True)