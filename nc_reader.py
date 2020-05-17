# coding: utf-8

import netCDF4 as nc
import numpy as np
import pandas as pd 
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px

class DataProc:
    def __init__(self, file_path):                    
        file_obj = nc.Dataset(file_path)

        self.longitude = file_obj.variables['longitude']
        self.latitude = file_obj.variables['latitude']
        self.time = file_obj.variables['time']
        self.land_mask = file_obj.variables['land_mask']
        self.temperature = file_obj.variables['temperature']
        self.climatology = file_obj.variables['climatology']
    def get_df(self,):
        tp = np.array(self.temperature)
        tp = pd.DataFrame(tp)
        tp['time_id']=tp.index
        tp = tp.melt(id_vars='time_id')
        tp = tp.rename(columns={'variable':'pt_id','value':'temperature'})

        lat,lon = np.array(self.latitude),np.array(self.longitude)
        lat,lon = pd.DataFrame(lat),pd.DataFrame(lon)
        lat['pt_id'] = lat.index
        lat = lat.rename(columns={0:'latitude'})
        lon['pt_id'] = lon.index
        lon = lon.rename(columns={0:'longitude'})

        t = np.array(self.time)
        t = pd.DataFrame(t)
        t['time_id'] = t.index
        t = t.rename(columns={0:'time'})

        df = tp.merge(t,how='left',on='time_id').merge(lat,how='left',on='pt_id').merge(lon,how='left',on='pt_id')
        df['pt'] = [(lat,lon) for lat,lon in zip(df['latitude'],df['longitude'])]
        df['year']=df['time']//1
        del df['pt_id']
        del df['time_id']
        del df['latitude']
        del df['longitude']
        del df['time']

        return df

if __name__ == "__main__":
    path = 'E:/Users/LuoZN/Desktop/Data_vis'
    equalarea = 'Raw_TAVG_EqualArea.nc'
    grid = 'Raw_TAVG_LatLong1.nc'
    file_path = os.path.join(path,equalarea)

    data_proc = DataProc(file_path)
    df = data_proc.get_df()
    df = df.groupby(by=['pt','year']).mean()

    df['latitude'] = [p[0][0] for p in df.index]
    df['longitude'] = [p[0][1] for p in df.index]
    df['year'] = [p[1] for p in df.index]
    df = df.reset_index(drop=True)

    #df = px.data.gapminder()
    fig = px.scatter_geo(df, lat = 'latitude', lon = 'longitude', color="temperature",
                projection="orthographic",animation_frame ='year')
    fig.show()
