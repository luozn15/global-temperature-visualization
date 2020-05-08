# coding=utf-8
import pandas as pd
import plotly
import plotly.express as px

path = 'maptemp.csv'
df = pd.read_csv(path)

fig = px.choropleth(df, locations="Code", color="AverageTemperature", hover_name="Country", animation_frame="dt",
color_continuous_scale=px.colors.sequential.Plasma)
fig.show()
