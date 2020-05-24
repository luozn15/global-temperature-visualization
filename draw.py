import data_proc
import pandas as pd
import os
import json
import pycountry
import plotly.express as px
import plotly

def draw_3dscatters():
    #path = os.path.abspath('./data')
    #equalarea = 'Raw_TAVG_EqualArea.nc'
    file_path = './data/Raw_TAVG_EqualArea.nc'#os.path.join(path,equalarea)

    df = data_proc.DataProc(file_path).get_df()
    df = df.groupby(by=['pt','year']).mean()

    df['latitude'] = [p[0][0] for p in df.index]
    df['longitude'] = [p[0][1] for p in df.index]
    df['year'] = [p[1] for p in df.index]
    df = df.reset_index(drop=True)

    #df = px.data.gapminder()
    fig = px.scatter_geo(df, lat = 'latitude', lon = 'longitude', color="temperature",
                projection="orthographic",animation_frame ='year')
    return fig

def draw_3d_earth(temperaturebycountry,year):  
    json_path = './data/countries.geo.json'

    with open(json_path) as j:
        countries = json.load(j)

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
    import data_proc
    csv_path = './data/GlobalLandTemperaturesByCountry.csv'
    tbc = data_proc.CSVReader(csv_path).tbc
    fig= draw_3d_earth(tbc,1890)
    fig.show()
 