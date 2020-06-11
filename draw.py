import data_proc
import pandas as pd
import os
import json
import pycountry
import plotly.express as px
import plotly
import data_proc

def draw_3d_earth(temperaturebycountry,year):  
    json_path = './data/countries.geo.json'
    geo_json = data_proc.JsonReader(json_path)
    countries = geo_json.countries

    temp=temperaturebycountry[temperaturebycountry['year']==year]
    fig = px.choropleth(temp, geojson=countries, locations='alpha_3', color='AverageTemperature',
                           featureidkey="id",projection="orthographic",
                           hover_name="country"
                          )
    fig.layout.title='全球气温变化相对值'
    fig.layout.coloraxis.colorbar.thickness=10
    #fig.layout.coloraxis.colorbar.orientation = 'h'
    fig.layout.coloraxis.colorbar.title.text = '全球气温变化相对值 (摄氏度)'
    fig.layout.coloraxis.colorbar.title.side = 'right'
    return fig, geo_json

def draw_line(df,alpha_3):#点击三维地球上的某个位置，出现展示该国的气温历史变化及预测分析的折线图，以及该国与周边区域对比的热力图。
    df_ = df[df['alpha_3']==alpha_3]
    fig = px.line(df_,x='year',y='AverageTemperature')
    fig.layout.title='国家历史气温走势'
    return fig

def draw_loc_scatters_LatLong1(year,longitude=120,lattitude=40):
    #path = os.path.abspath('./data')
    #equalarea = 'Raw_TAVG_EqualArea.nc'
    #nc_path = './data/Raw_TAVG_EqualArea.nc'
    nc_path = './data/Raw_TAVG_LatLong1.nc'
    df = data_proc.NCProc_LatLong1(nc_path).get_year(int(year))

    fig = px.scatter_geo(df, lat = 'latitude', lon = 'longitude', color="temperature", projection="orthographic")
    fig.layout.geo.center=dict(lon=longitude,lat=lattitude)
    fig.layout.geo.projection.scale=5
    return fig

def draw_loc_scatters_EqualArea(df,year,longitude=120,lattitude=40):
    #path = os.path.abspath('./data')
    #equalarea = 'Raw_TAVG_EqualArea.nc'
    #nc_path = './data/Raw_TAVG_EqualArea.nc'
    #nc_path = './data/Raw_TAVG_EqualArea.nc'
    #df = data_proc.NCProc_EqualArea(nc_path).get_df()

    fig = px.scatter_geo(df.query('year=='+str(year)), lat = 'latitude', lon = 'longitude',
                         color="temperature",projection="conic equal area",color_continuous_scale="Viridis")
    fig.layout.geo.center=dict(lon=longitude,lat=lattitude)
    fig.layout.geo.projection.scale=5
    fig.layout.title='局部地区气温变化相对值'
    fig.layout.coloraxis.colorbar.thickness=7
    fig.layout.coloraxis.colorbar.len = .6
    fig.layout.coloraxis.colorbar.title.text = '局部地区气温变化相对值 (摄氏度)'
    fig.layout.coloraxis.colorbar.title.side = 'right'
    fig.layout.margin.b=10
    return fig

def draw_bar_latitude(df,year):
    df = df.query("year=="+str(year))
    df_ = df.groupby('latitude')['temperature'].mean().reset_index(drop=False)
    fig = px.bar(df_, x="latitude", y="temperature",color="temperature",
                color_continuous_scale="Viridis")
    fig.layout.title='纬度气温变化相对值'
    fig.update_layout(coloraxis_showscale=False)
    return fig

if __name__ == "__main__":
    
    #csv_path = './data/GlobalLandTemperaturesByCountry.csv'
    #tbc = data_proc.CSVReader(csv_path).tbc
    #fig= draw_3d_earth(tbc,1890)
    nc_path = './data/Raw_TAVG_EqualArea.nc'
    df = data_proc.NCProc_EqualArea(nc_path).get_df()
    fig = draw_bar_latitude(df,'1890')
    #print(fig)
    fig.show()
 