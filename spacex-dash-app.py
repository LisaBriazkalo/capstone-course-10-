# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites_list=pd.unique(spacex_df['Launch Site'])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown', options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': launch_sites_list[0], 'value': launch_sites_list[0]},
                                    {'label': launch_sites_list[1], 'value': launch_sites_list[1]},
                                    {'label': launch_sites_list[2], 'value': launch_sites_list[2]},
                                    {'label': launch_sites_list[3], 'value': launch_sites_list[3]}
                                    ],
                                    value='ALL',
                                    placeholder="Choose the Launch Site",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 2000: '2000', 4000: '4000', 
                                6000: '6000', 8000: '8000', 10000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches for All Sites')
        return fig
    else:
        fig = px.pie(filtered_df,
        names='class', 
        title='Total Success Launches for Site '+entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_point(entered_site, entered_mass):
    filtered_df=spacex_df[(spacex_df['Payload Mass (kg)']>=entered_mass[0]) & (spacex_df['Payload Mass (kg)']<=entered_mass[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
        color="Booster Version Category", 
        title='Corellation between Payload Mass and Success for All Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
        color="Booster Version Category", 
        title='Corellation between Payload Mass and Success for'+entered_site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run()
