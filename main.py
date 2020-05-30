import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
#import pandas as pd
import os

import draw
import data_proc

if __name__ == "__main__":      
    
    #os.chdir('./global-temperature-visualization')  
    csv_path = './data/GlobalLandTemperaturesByCountry.csv'
    tbc = data_proc.CSVReader(csv_path).tbc
    fig1 = draw.draw_3d_earth(tbc,tbc['year'].min())
    fig1.layout.height=800
    fig2 = draw.draw_line(tbc,'CHN')
    fig2.layout.height=400
    fig3 = draw.draw_loc_scatters(tbc['year'].max())
    fig3.layout.height=400

    #external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash()
    app.layout = html.Div([
        html.H1('全球地表气温可视化',
                style={'textAlign': 'center'}
        ),
        html.Div(children='大数据可视化大作业 by 熊鑫昌 许家声 罗子牛',
                style={'textAlign': 'center'}
        ),

        html.Div([
            dcc.Graph(id='3d_earth',figure=fig1)],
                style={'width': '64%','height':'100%','display': 'inline-block'}
        ),

        html.Div([
        html.Div([
            dcc.Graph(id='line',figure=fig2)], 
                style={'width': '100%','height':'49%'}
        ),
        
        html.Div([
            dcc.Graph(id='local_scatter',figure=fig3)],
                style={'width': '100%','height':'49%'}
        ),],style={'width': '34%','height':'100%','display': 'inline-block'})
    ])

    '''@app.callback(
        Output(component_id='3d_earth', component_property='figure'),
        [Input(component_id='year-slider', component_property='value')]
    )
    def update_3d_earth(selected_year):
        fig = draw.draw_3d_earth(tbc,selected_year)
        return fig'''

    @app.callback(
        Output(component_id='3d_earth', component_property='figure'),
        [Input(component_id='line', component_property='clickData')]
    )
    def update_3d_earth(clickData):
        if clickData:
            year = clickData['points'][0]['x']
            fig1 = draw.draw_3d_earth(tbc,year)
            return fig1
        else:
            fig1 = draw.draw_3d_earth(tbc,tbc['year'].min())
            return fig1

    @app.callback(
        Output(component_id='line',component_property='figure'),
        [Input(component_id='3d_earth',component_property='clickData')]
    )
    def update_line(clickData):
        if clickData:
            print(clickData)
            alpha_3 = clickData['points'][0]['location']
            fig2 = draw.draw_line(tbc,alpha_3)
            return fig2
        else:
            fig2 = draw.draw_line(tbc,'CHN')
            return fig2

    app.run_server(debug=True)