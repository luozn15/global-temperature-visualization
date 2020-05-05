import plotly_express as px
import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv('temptest.csv',delimiter=',')

fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Date"], y=data["Anomaly"],
                    mode='lines',
                    name='Average temperature'))
moving = data["Anomaly"].rolling(12).mean()
fig.add_trace(go.Scatter(x=data["Date"], y=moving,
                    mode='lines',
                    name='Moving average of average temperature'))

#fig.add_trace(go.Scatter(x=data["Date"], y=data["Max"],
#                    mode='lines',
#                    name='Average high temperature'))
#moving = data["Max"].rolling(12).mean()
#fig.add_trace(go.Scatter(x=data["Date"], y=moving,
#                    mode='lines',
#                    name='Moving average of average high temperature'))
                    
#fig.add_trace(go.Scatter(x=data["Date"], y=data["Min"],
#                    mode='lines',
#                    name='Average low temperature'))
#moving = data["Min"].rolling(12).mean()
#fig.add_trace(go.Scatter(x=data["Date"], y=moving,
#                    mode='lines',
#                    name='Moving average of average low temperature'))
                    
                    
fig.update_layout(title='Temperature of global land',
xaxis_title='Year',
yaxis_title='Temperature (degrees Celsius)')

fig.show()
