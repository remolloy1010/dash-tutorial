# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas

# incorporate data into app
# Source - https://www.cdc.gov/nchs/pressroom/stats_of_the_states.htm
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Good_to_Know/Dash2.0/social_capital.csv")
print(df.head())
print(df['YEAR'].unique())
# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
# dropdown = dcc.Dropdown(options=df.columns.values[2:],
#                         value='Cesarean Delivery Rate',  # initial value displayed when page first loads
#                         clearable=False)

dropdown_charttype = dcc.Dropdown(value='Map',
                                  options=['Map', 'Bar Chart', 'Line Chart'],
                                  clearable=False)
dropdown_year = dcc.Dropdown(value=df['YEAR'].unique()[-1],
                             options=df['YEAR'].unique(),
                             clearable=False)

dropdown_state = dcc.Dropdown(value=df['STATE'].unique()[0],
                              options=df['STATE'].unique(),
                              clearable=False)


# Customize your own Layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([mytitle], width=10),
            dbc.Col([dropdown_charttype], width=2)
        ], justify='center'),
        dbc.Row([
            dbc.Col([mygraph], width=12)
        ]),
        dbc.Row([
            html.Div([
                dbc.Col(dcc.Dropdown(id='dropdown', options=df.columns.values[2:],
                        value='Cesarean Delivery Rate',  # initial value displayed when page first loads
                        clearable=False), width=4)
            ], style={'display' : 'none'})

        ], justify='center'),
        dbc.Row([
            dbc.Col([dropdown_year], width=2),
            dbc.Col([dropdown_state], width=2)
        ]),
        # html.Div([
        #         # Create element to hide/show, in this case an 'Input Component'
        #         dcc.Input(
        #         id = 'element-to-hide',
        #         placeholder = 'something',
        #         value = 'Can you see me?',
        #         )
        #     ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
        #     )


    ], fluid=True)
])

# Callback allows components to interact
@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    # Output(component_id='element-to-hide', component_property='style'),
    Input('dropdown', 'value'),
    Input(dropdown_charttype, 'value'),
    Input(dropdown_year, 'value'),
    Input(dropdown_state, 'value')
)
def update_graph(column_name, chart_type, year, state):  # function arguments come from the component property of the Input

    print(column_name)
    print(type(column_name))
    # https://plotly.com/python/choropleth-maps/
    if chart_type == 'Bar Chart':
        fig = px.bar(data_frame=df[df['YEAR'] == year], x="STATE", y=column_name)
        # style_on_off = 'none'
    elif chart_type == 'Map':
        fig = px.choropleth(data_frame=df,
                            locations='STATE',
                            locationmode="USA-states",
                            scope="usa",
                            height=600,
                            color=column_name,
                            animation_frame='YEAR')
        # style_on_off = 'none'
    elif chart_type == 'Line Chart':
        fig = px.line(data_frame=df[df['STATE'] == state], x="YEAR", y=column_name, color='STATE', markers=True)
        # style_on_off = 'block'

    # if value == 'on':
    #     style_on_off = {'display': 'block'}
    # elif value == 'off':
    #     style_on_off = {'display': 'none'}


    return fig, '# '+column_name  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)