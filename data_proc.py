# coding: utf-8
import netCDF4 as nc
import numpy as np
import pandas as pd 
import os
import pycountry
import json

class NCProc:
    def __init__(self, file_path):                    
        file_obj = nc.Dataset(file_path)
        self.obj = file_obj
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

class NCProc2:
    def __init__(self, file_path):                    
        file_obj = nc.Dataset(file_path)
        self.nc = file_obj
        self.longitude = file_obj.variables['longitude']
        self.latitude = file_obj.variables['latitude']
        self.time = file_obj.variables['time']
        self.land_mask = file_obj.variables['land_mask']
        self.temperature = file_obj.variables['temperature']
        self.climatology = file_obj.variables['climatology']
    def get_year(self,year):
        lat = np.array(self.latitude)
        long = np.array(self.longitude)
        index = np.array(self.time)//1 == year
        tp = np.nanmean(np.array(self.temperature)[index],axis=0)
        df = pd.DataFrame(tp.reshape(len(lat)*len(long)),columns=['temperature'])
        df['latitude'] = lat.repeat(len(long))
        df['longitude'] = np.tile(long,len(lat))
        return df

class CSVReader:
    def __init__(self,file_path):
        self.tbc = self.proc_csv(file_path)
    def proc_csv(self,file_path):
        temperaturebycountry = pd.read_csv(file_path)
        del temperaturebycountry['AverageTemperatureUncertainty']
        temperaturebycountry['dt'] = pd.to_datetime(temperaturebycountry['dt']) 
        temperaturebycountry['year'] = [int(date.year) for date in temperaturebycountry.dt]
        del temperaturebycountry['dt']
        temperaturebycountry['Country'] = [name.split(' (')[0] for name in temperaturebycountry['Country']]
        temperaturebycountry =  temperaturebycountry.groupby(['Country','year']).mean()
        temperaturebycountry['country'] = [p[0] for p in temperaturebycountry.index]
        temperaturebycountry['year'] = [int(p[1]) for p in temperaturebycountry.index]
        temperaturebycountry = temperaturebycountry.reset_index(drop=True)
        temperaturebycountry = temperaturebycountry.drop(temperaturebycountry[temperaturebycountry['country']=='Taiwan'].index)

        alpha_3 = {}
        for c in list(set(temperaturebycountry['country'])):
            try:
                a = pycountry.countries.get(name = c).alpha_3
                alpha_3[c] = a
            except:
                try:
                    a = pycountry.countries.get(common_name = c).alpha_3
                    alpha_3[c] = a
                except:
                    pass
        temperaturebycountry['alpha_3'] = temperaturebycountry['country'].map(alpha_3)
        temperaturebycountry = temperaturebycountry[temperaturebycountry['alpha_3'].notna()]
        return temperaturebycountry

class JsonReader:
    def __init__(self,json_path):
        with open(json_path) as j:
            self.countries = json.load(j)
    def get_center(self):
        center = {}
        for country in self.countries['features']:
            if country['geometry']['type'] =='Polygon':
                center[country['id']] = np.array(country['geometry']['coordinates'][0]).mean(axis=0)
            elif country['geometry']['type'] =='MultiPolygon':
                center[country['id']] = np.array([np.array(p[0]).mean(axis=0) for p in country['geometry']['coordinates']]).mean(axis=0)
        return center

if __name__ == "__main__":
    #csv_path = './data/GlobalLandTemperaturesByCountry.csv'
    #print(CSVReader(csv_path).tbc)
    nc_path = './data/Raw_TAVG_LatLong1.nc'
    print(NCProc2(nc_path).get_year(1890))