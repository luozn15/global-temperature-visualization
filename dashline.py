# coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import os

if __name__ == "__main__":
    path = 'temptest.csv'
    data = pd.read_csv(path)

    #Code 为国家缩写，plotly_express 用缩写来识别国家位置
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Anomaly"],
                        mode='lines',
                        name='Average temperature'))
    moving = data["Anomaly"].rolling(12).mean()
    fig.add_trace(go.Scatter(x=data["Date"], y=moving,
                        mode='lines',
                        name='Moving average of average temperature'))

    #fig.add_trace(go.Scatter(x=data["Date"], y=data["Max"],
    #                    mode='lines',
    #                    name='Average high temperature'))
    #moving = data["Max"].rolling(12).mean()
    #fig.add_trace(go.Scatter(x=data["Date"], y=moving,
    #                    mode='lines',
    #                    name='Moving average of average high temperature'))
                        
    #fig.add_trace(go.Scatter(x=data["Date"], y=data["Min"],
    #                    mode='lines',
    #                    name='Average low temperature'))
    #moving = data["Min"].rolling(12).mean()
    #fig.add_trace(go.Scatter(x=data["Date"], y=moving,
    #                    mode='lines',
    #                    name='Moving average of average low temperature'))

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    app.run_server(debug=True)

