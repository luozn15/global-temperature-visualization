import numpy as np
import pandas as pd
import plotly
import plotly.express as px
#读取数据
path = '.\\GlobalLandTemperaturesByCountry.csv'
df = pd.read_csv(path)
#删除空值
#df = df[df['AverageTemperature'].notna()]
df = df.dropna(axis=0, how='any', subset=['AverageTemperature'])
#添加年份信息
dt = list(df['dt'])
year_lst = []
for i in dt:
    dt_year = i.split('-')[0]
    year_lst.append(dt_year)
df.loc[:,'year'] = year_lst


#各年平均气温（1750-2012）
year = sorted(list(set(df['year'])))
country = list(set(df['Country']))
df_year = pd.DataFrame()
for i in country:
    df_cou = df[df['Country']==str(i)]
    for j in year:
        df_tem = df_cou[df_cou['year']==j]
        tem_lst = list(df_tem['AverageTemperature'])
        if len(tem_lst)>0:
            Aver_Temp = np.mean(tem_lst)
            #print('Aver_Temp',Aver_Temp)
            df_tem2 = pd.DataFrame([[j,i,Aver_Temp]], columns=['year', 'country','AverageTemperature'])
            #print('df_tem2',df_tem2)
            df_year = df_year.append(df_tem2, ignore_index=True)

start = 1850
end = 2013
df_record = df_year[df_year['year']==str(start)]
country_record = list(set(df_record['country']))
df_rise = pd.DataFrame()
for i in country_record:
    df_cou2 = df_year[df_year['country']==i]
    start_temp = []
    end_temp = []
    #取start（包括）之后五年气温的平均值
    m = 0
    p = 0
    while m<5:
        single_year = start + p
        start_single = list(df_cou2[df_cou2['year']==str(single_year)]['AverageTemperature'])
        if len(start_single)==0:
            p = p + 1
            m = m
        else:
            start_temp.append(float(start_single[0]))
            m = m + 1
    start_temp = np.mean(start_temp)
    #取end（不包括）之前五年的平均值
    for n in range(end-5,end):
        end_single = list(df_cou2[df_cou2['year']==str(n)]['AverageTemperature'])[0]
        end_temp.append(float(end_single))
    end_temp = np.mean(end_temp)
    rise_temp = end_temp - start_temp
    df_tem3 = pd.DataFrame([[i,rise_temp]], columns=['country','rise_temp'])
    df_rise = df_rise.append(df_tem3, ignore_index=True)
#按气温变化值降序排序
df_rise = df_rise.sort_values('rise_temp',ascending=False)
#各国气温变化条形图（1750-2012）
df_bar = df_rise.head(50)
fig = px.bar(df_bar, x="country", y="rise_temp", color="rise_temp",title='1850—2012年各国气温变化条形图（前50）',
             color_continuous_scale=px.colors.sequential.Inferno)
plotly.offline.plot(fig, filename='1850—2012年各国气温变化折条形图（前50）.html')

