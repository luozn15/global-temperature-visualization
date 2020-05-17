import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd
import os
import nc_reader

if __name__ == "__main__":        
    path = 'E:/Users/LuoZN/Desktop/Data_vis'
    equalarea = 'Raw_TAVG_EqualArea.nc'
    grid = 'Raw_TAVG_LatLong1.nc'
    file_path = os.path.join(path,equalarea)

    data_proc = nc_reader.DataProc(file_path)
    df = data_proc.get_df()
    df = df.groupby(by=['pt','year']).mean()

    df['latitude'] = [p[0][0] for p in df.index]
    df['longitude'] = [p[0][1] for p in df.index]
    df['year'] = [p[1] for p in df.index]
    df = df.reset_index(drop=True)

    fig = px.scatter_geo(df, lat = 'latitude', lon = 'longitude', color="temperature",
                projection="orthographic",animation_frame ='year')

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.Div([
            dcc.Graph(figure=fig)
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ])
    app.run_server(debug=True)
