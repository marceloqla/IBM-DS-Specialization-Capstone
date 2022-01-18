# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

site_names = list(set(list(spacex_df['Launch Site'])))

site_dict_list = []
site_obj = {'label':'','value':''}
site_dict_list.append(site_obj.copy())
site_dict_list[-1]['label'] = 'All Sites'
site_dict_list[-1]['value'] = 'ALL'
for name in site_names:
    site_dict_list.append(site_obj.copy())
    site_dict_list[-1]['label'] = name
    site_dict_list[-1]['value'] = name
    
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36',
        'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(id='site-dropdown', options=site_dict_list,
        value='ALL',placeholder='Select a Launch Site here',searchable=True),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=[min_payload, max_payload]),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(data, values='counts', 
        names='class', 
        title='Success rate for all sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        data = filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(data, values='counts', 
        names='class', 
        title=f"Success rate for site {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, entered_range):
    filtered_df = spacex_df
    data = filtered_df[filtered_df['Payload Mass (kg)'] >= entered_range[0]]
    data = data[data['Payload Mass (kg)'] <= entered_range[1]]
    if entered_site == 'ALL':
        fig = px.scatter(data, x='Payload Mass (kg)', 
        y='class', 
        title='Success rate for Payload Mass (kg) - All Sites',
        color="Booster Version Category")
        return fig
    else:
        data = data[data['Launch Site'] == entered_site]
        fig = px.scatter(data, x='Payload Mass (kg)', 
        y='class', 
        title='Success rate for Payload Mass (kg) - All Sites',
        color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
