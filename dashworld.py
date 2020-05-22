# coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd
import os

if __name__ == "__main__":
    path = 'maptemp.csv'
    df = pd.read_csv(path)

    #Code 为国家缩写，plotly_express 用缩写来识别国家位置
    fig = px.choropleth(df, locations="Code", color="AverageTemperature", hover_name="Country", animation_frame="dt",
    color_continuous_scale=px.colors.sequential.Plasma)

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    app.run_server(debug=True)

