from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas

# incorporate data into app
# Source - https://www.cdc.gov/nchs/pressroom/stats_of_the_states.htm
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Good_to_Know/Dash2.0/social_capital.csv")


app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df.columns.values[2:],
                        value='Cesarean Delivery Rate',  # initial value displayed when page first loads
                        clearable=False)

dropdown_charttype = dcc.Dropdown(value='Map',
                                  options=['Map', 'Bar Chart', 'Line Chart'],
                                  clearable=False)
dropdown_year = dcc.Dropdown(value=df['YEAR'].unique()[-1],
                             options=df['YEAR'].unique(),
                             clearable=False)

# dropdown_state = dcc.Dropdown(value=df['STATE'].unique()[0],
#                               options=df['STATE'].unique(),
#                               clearable=False)
app.layout = html.Div([
    dcc.Dropdown(
        id = 'dropdown-to-show_or_hide-element',
        options=[
            {'label': 'Show element', 'value': 'on'},
            {'label': 'Hide element', 'value': 'off'}
        ],
        value = 'off'
    ),

    # Create Div to place a conditionally visible element inside
    html.Div([
        dcc.Dropdown(value=df['STATE'].unique()[0],
                     options=df['STATE'].unique(),
                     clearable=False)
        # Create element to hide/show, in this case an 'Input Component'
        # dcc.Input(
        # id = 'element-to-hide',
        # placeholder = 'something',
        # value = 'Can you see me?',
        # )
    ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
    ),
    # dbc.Container([
    #     dbc.Row([
    #         dbc.Col([mytitle], width=10),
    #         dbc.Col([dropdown_charttype], width=2)
    #     ], justify='center'),
    #     dbc.Row([
    #         dbc.Col([mygraph], width=12)
    #     ]),
    #     dbc.Row([
    #         dbc.Col([dropdown], width=4)
    #     ], justify='center'),
    #     dbc.Row([
    #         dbc.Col([dropdown_year], width=2),
    #         dbc.Col([dropdown_state], width=2)
    #     ])
    # ])
])

@app.callback(
    Output(component_id='element-to-hide', component_property='style'),
    # Output(mygraph, 'figure'),
    # Output(mytitle, 'children'),
    # Input(dropdown, 'value'),
    # Input(dropdown_charttype, 'value'),
    # Input(dropdown_year, 'value'),
    # Input(dropdown_state, 'value'),
    [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])

def show_hide_element(value):
    if value == 'on':
        return {'display': 'block'}
    if value == 'off':
        return {'display': 'none'}

if __name__ == '__main__':
    app.server.run(debug=False)