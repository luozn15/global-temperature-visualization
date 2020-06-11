import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
#import pandas as pd
import os
import numpy as np

import draw
import data_proc

if __name__ == "__main__":      
    
    #os.chdir('./global-temperature-visualization')  
    csv_path = './data/GlobalLandTemperaturesByCountry.csv'
    tbc = data_proc.CSVReader(csv_path).tbc
    nc_path = './data/Raw_TAVG_EqualArea.nc'
    df_EqualArea = data_proc.NCProc_EqualArea(nc_path).get_df()

    fig1_origin, geo_json = draw.draw_3d_earth(tbc,tbc['year'].max())
    fig1_origin.layout.height=700
    fig2_origin = draw.draw_loc_scatters_EqualArea(df_EqualArea,tbc['year'].max(),110,40)
    fig2_origin.layout.height= 300
    fig3_origin = draw.draw_line(tbc,'CHN')
    fig3_origin.layout.height=300
    fig4_origin = draw.draw_bar_latitude(df_EqualArea,tbc['year'].max())
    fig4_origin.layout.height=250

    marks = {i:str(i) for i in np.sort(tbc['year'].unique()) if (i % 20== 0)}
    c_a = tbc[['country','alpha_3']].drop_duplicates().reset_index(drop=True)
    country_options = [{'label': c, 'value': a} for c,a in zip(c_a['country'],c_a['alpha_3'])]

    #external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.Div([
            html.H1(
                children='全球地表气温可视化',
                style={'textAlign': 'center',"marginBottom": "0px"}),
            html.H3(
                children='数据可视化大作业 by 熊鑫昌 许家声 罗子牛',
                style={'textAlign': 'center',"marginTop": "0px"}),],
            style={'marginBottom':'25px'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Div(
                        children='全球气温年份：'+str(tbc['year'].max())+'年',
                        id = 'year_label',
                        style={'display':'block','textAlign': 'center',
                            'marginTop':'15px','width':'30%'}),
                    html.Div([
                        dcc.Slider(id='year_slider',
                            min=tbc['year'].min(),
                            max=tbc['year'].max(),
                            step=1,
                            marks={1760: '1760',
                                    1780: '1780',
                                    1800: '1800',
                                    1820: '1820',
                                    1840: '1840',
                                    1860: '1860',
                                    1880: '1880',
                                    1900: '1900',
                                    1920: '1920',
                                    1940: '1940',
                                    1960: '1960',
                                    1980: '1980',
                                    2000: '2000'},
                            value=tbc['year'].max())],
                        style={'display':'block','textAlign': 'center','margin':'10px',
                            'padding':'auto','width':'70%'})],
                    style={'display':'flex','flexDirection':'row',"margin":"10px","borderRadius": "15px",
                        'backgroundColor': '#ffffff',"padding":"15px","paddingTop":"10px","boxShadow":"2px 2px 2px lightgrey"}),
                html.Div([
                    dcc.Graph(id='3d_earth',figure=fig1_origin)],
                    style={'display':'block','margin':'20px',"margin":"10px",
                        "borderRadius": "15px",'backgroundColor': '#ffffff',
                        "padding":"10px","boxShadow":"2px 2px 2px lightgrey",}),
                html.Div([
                    dcc.Graph(id='bar',figure=fig4_origin)], 
                    style={'display':'block',"borderRadius": "15px",
                        'backgroundColor': '#ffffff',"margin":"10px",
                        "padding":"10px","boxShadow":"2px 2px 2px lightgrey",})],
                style={'display':'flex','flexDirection':'column','width':'60%'}),
            html.Div([
                html.Div(
                    [html.Div(
                        children='国家alpha_3编码：'+'CHN',
                        id = 'alpha3_country',
                        style={'width': '50%','textAlign':'center',"borderRadius": "15px",
                            'backgroundColor': '#ffffff',"margin":"10px",
                            "padding":"20px","boxShadow":"2px 2px 2px lightgrey",}),
                    html.Div(
                        dcc.Dropdown(
                            id='name_country',
                            options=country_options,
                            value='CHN'),
                        style={'width': '50%',"borderRadius": "15px",
                    'backgroundColor': '#ffffff',"margin":"10px",
                    "padding":"10px","boxShadow":"2px 2px 2px lightgrey",})],
                    style={'display':'flex','flexDirection':'row',}),
                html.Div([
                    dcc.Graph(id='local_scatter',figure=fig2_origin)],
                    style={'display':'block',"borderRadius": "15px",
                        'backgroundColor': '#ffffff',"margin":"10px",
                        "padding":"10px","boxShadow":"2px 2px 2px lightgrey",}),
                html.Div([
                    dcc.Graph(id='line',figure=fig3_origin)], 
                    style={'display':'block',"borderRadius": "15px",
                        'backgroundColor': '#ffffff',"margin":"10px",
                        "padding":"10px","boxShadow":"2px 2px 2px lightgrey",}),
                html.Div(
                    children='summary', 
                    style={'display':'block',"borderRadius": "15px",
                        'backgroundColor': '#ffffff',"margin":"10px",
                        "padding":"30px","boxShadow":"2px 2px 2px lightgrey",
                        'height':'250px'})],
                style={'display':'flex','flexDirection':'column','width':'35%'})],
            style={"display": "flex",'flexDirection':'row'})
    ],
    style={"display": "flex",'flexDirection':'column',
        'padding':'5%','margin':'0px','backgroundColor':'#f2f2f2',
        'fontWeight':'400'})

    '''@app.callback(
        Output(component_id='3d_earth', component_property='figure'),
        [Input(component_id='year-slider', component_property='value')]
    )
    def update_3d_earth(selected_year):
        fig = draw.draw_3d_earth(tbc,selected_year)
        return fig'''

    @app.callback(
        [Output(component_id='year_label', component_property='children'),
        Output(component_id='3d_earth', component_property='figure'),
        Output(component_id='bar', component_property='figure')],
        [Input(component_id='year_slider', component_property='value')]
    )
    def update_year(year):
        year_label = '全球气温年份：'+str(year)+'年'
        fig1, _ = draw.draw_3d_earth(tbc,year)
        fig4 = draw.draw_bar_latitude(df_EqualArea,year)
        return year_label,fig1,fig4


    @app.callback(
        [Output(component_id='name_country', component_property='value'),
        Output(component_id='alpha3_country',component_property='children'),
        Output(component_id='line', component_property='figure')],
        [Input(component_id='3d_earth',component_property='clickData'),
        Input(component_id='year_label',component_property='children')]
    )
    def update_country(clickData_earth, year_label):
        if clickData_earth :
            year = year_label.split('：')[1].split('年')[0]
            alpha_3 = clickData_earth['points'][0]['location']
            alpha3_country= '国家alpha_3编码：'+alpha_3
            fig3 = draw.draw_line(tbc,alpha_3)  
            return alpha_3,alpha3_country,fig3
        else:
            return 'CHN','国家alpha_3编码：CHN',fig3_origin

    @app.callback(
        Output(component_id='local_scatter',component_property='figure'),
        [Input(component_id='alpha3_country', component_property='children'),
        Input(component_id='year_label',component_property='children'),]
    )
    def update_fig2(alpha3_country, year_label):
        year = year_label.split('：')[1].split('年')[0]
        alpha_3 = alpha3_country.split('：')[1]
        center = geo_json.get_center_alpha3(alpha_3)
        fig2 = draw.draw_loc_scatters_EqualArea(df_EqualArea,year,center[0],center[1])
        return fig2

    app.run_server(debug=True)