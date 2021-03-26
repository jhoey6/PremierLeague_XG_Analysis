# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import base64

PLxG_21 = pd.read_csv('adv_shooting_PL_21.csv')

# Create a dash application
app = JupyterDash(__name__)
#JupyterDash.infer_jupyter_proxy_config()
#app.config.suppress_callback_exceptions = True
test_png = 'pl_img.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

#formatting
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

team_dropdown = [{'label': 'Arsenal', 'value': 'ARS'},
                 {'label': 'Aston Villa', 'value': 'AVL'},
                 {'label': 'Brighton', 'value': 'BHA'},
                 {'label': 'Burnley', 'value': 'BUR'},
                 {'label': 'Crystal Palace', 'value': 'CPY'},
                 {'label': 'Everton', 'value': 'EVE'},
                 {'label': 'Fulham', 'value': 'FUL'},
                 {'label': 'Leeds United', 'value': 'LEE'},
                 {'label': 'Leicester City', 'value': 'LEI'},
                 {'label': 'Liverpool', 'value': 'LVP'},
                 {'label': 'Manchester City', 'value': 'MNC'},
                 {'label': 'Manchester United', 'value': 'MNU'},
                 {'label': 'Newcastle United', 'value': 'NEW'},
                 {'label': 'Sheffield United', 'value': 'SHE'},
                 {'label': 'Southampton', 'value': 'SOU'},
                 {'label': 'Tottenham Hotspurs', 'value': 'TOT'},
                 {'label': 'West Bromich Albion', 'value': 'WBA'},
                 {'label': 'West Ham United', 'value': 'WHA'},
                 {'label': 'Wolverhampton Wanderers', 'value': 'WOL'}
                ]

app.layout = html.Div(children=[
    html.Div([
        html.H1('Premier Leauge 2020-2021 Advanced Shooting Dashboard', style={'textAlign': 'center', 'font-size': 40}),
        html.Img(src='data:image/png;base64,{}'.format(test_base64))       
    ], style={'display': 'flex', 'color': colors['text']}),
     
    html.Div(className = 'toggle', children=[
        html.Div(
        dcc.Dropdown(id='team-select',
                    options = team_dropdown,
                    placeholder='Select Teams',
                    #style={'width':'50%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'},
                    value = ['ARS', 'AVL'],
                    multi=True)),
        html.Div(
        dcc.RangeSlider(id='matchday-range',
                       min=1,
                       max=36,
                       step=1,
                       value=[1, 36],
                       marks = {x:x for x in set(PLxG_21['Round'])},
                       allowCross=False))
        
    ]),
    
    html.Div(dcc.Graph(id='plot1')),
    html.Div(dcc.Graph(id='plot2'))
        
    ])

@app.callback([Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2', component_property='figure')],
              [Input(component_id='team-select', component_property='value'),
              Input(component_id='matchday-range', component_property='value')])
def matchday_xG(teams, rounds):
    df_rounds = PLxG_21[PLxG_21['Round'].between(rounds)]
    if type(teams) == 'str':
        df_teams = df_rounds[df_rounds['Team'] == teams]
    else:
        df_teams = df_rounds[df_rounds['Team'].isin(teams)]
        
    rounds_grouped = df_rounds.groupby('Team').mean().rest_index
    
    xG_trend = px.area(df_teams, x='Round', y='xG', color='Team')
    xG_v_GF = px.scatter(rounds_grouped, x='xG', y='GF', color='Team')
    return xG_trend, xG_v_GF

# Run the app
if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
    app.run_server(port="5000", host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)
              