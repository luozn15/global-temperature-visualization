import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly 

app = dash.Dash()
app.layout = html.Div([
    html.H1('全球地表气温可视化',
            style={'textAlign': 'center'}
    ),
    html.Div(children='大数据可视化大作业 by 熊鑫昌 许家声 罗子牛',
            style={'textAlign': 'center'}
    ),

    html.Div([
        dcc.Graph(id='3d_earth')],
            style={'width': '49%','height':'100%','display':'inline-block'}
    ),
    html.Div([
    html.Div([
        dcc.Graph(id='line')], 
            style={'width': '100%','height':'49%'}
        ),
    html.Div([
        dcc.Graph(id='line2')], 
            style={'width': '100%','height':'49%'}
        )],
        style={'width': '49%','height':'100%','display':'inline-block'}
    )
])

app.run_server(debug=True)
