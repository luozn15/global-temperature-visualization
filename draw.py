import data_proc
import pandas as pd
import os
import json
import pycountry
import plotly.express as px
import plotly
import data_proc

def draw_loc_scatters(year):
    #path = os.path.abspath('./data')
    #equalarea = 'Raw_TAVG_EqualArea.nc'
    #nc_path = './data/Raw_TAVG_EqualArea.nc'
    nc_path = './data/Raw_TAVG_LatLong1.nc'

    df = data_proc.NCProc2(nc_path).get_year(int(year))

    fig = px.scatter_geo(df, lat = 'latitude', lon = 'longitude', color="temperature")
    #fig = px.scatter_mapbox(df, lat='latitude', lon='latitude', color="temperature",zoom=10)
    fig.layout.height=400
    return fig

def draw_3d_earth(temperaturebycountry,year):  
    json_path = './data/countries.geo.json'
    countries = data_proc.JsonReader(json_path).countries

    temp=temperaturebycountry[temperaturebycountry['year']==year]
    fig = px.choropleth(temp, geojson=countries, locations='alpha_3', color='AverageTemperature',
                           featureidkey="id",color_continuous_scale="Viridis",projection="orthographic",
                           hover_name="country"
                          )
    return fig

def draw_line(df,alpha_3):#点击三维地球上的某个位置，出现展示该国的气温历史变化及预测分析的折线图，以及该国与周边区域对比的热力图。
    df_ = df[df['alpha_3']==alpha_3]
    fig = px.line(df_,x='year',y='AverageTemperature')
    return fig

if __name__ == "__main__":
    
    csv_path = './data/GlobalLandTemperaturesByCountry.csv'
    tbc = data_proc.CSVReader(csv_path).tbc
    fig= draw_3d_earth(tbc,1890)
    #fig = draw_loc_scatters('1890')
    print(fig)
    fig.show()
 