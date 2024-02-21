# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
launch_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = launch_df['Payload Mass (kg)'].max()
min_payload = launch_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # dcc.Dropdown(id='site-dropdown',...)
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'ALL SITES', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    value=[min_payload, max_payload],
                    marks={0: '0', 2500: '2500', 5000: '5000',
                           7500: '7500', 10000: '10000'}),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def build_graph(site_dropdown):
    if site_dropdown == 'ALL':
        labels = launch_df['Launch Site'].unique()
        values = launch_df['class'].value_counts().values
        piechart = go.Figure(data=[go.Pie(labels=labels, values=values)])
        piechart.update_layout(title='Total Launches for All Sites')
        return piechart
    else:
        specific_df = launch_df.loc[launch_df['Launch Site'] == site_dropdown]
        labels = specific_df['class'].value_counts().index.tolist()
        values = specific_df['class'].value_counts().values.tolist()
        piechart = go.Figure(data=[go.Pie(labels=labels, values=values)])
        piechart.update_layout(title='Total Launch for a Specific Site')
        return piechart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def update_graph(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        filtered_data = launch_df[(launch_df['Payload Mass (kg)'] >= payload_slider[0])
                                  & (launch_df['Payload Mass (kg)'] <= payload_slider[1])]
        scatterplot = go.Figure(data=go.Scatter(x=filtered_data["Payload Mass (kg)"], y=filtered_data["class"],
                                                mode='markers', marker=dict(color="Booster Version Category")))
        scatterplot.update_layout(title='Correlation between Payload and Launch Success',
                                  xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        return scatterplot
    else:
        specific_df = launch_df.loc[launch_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[(specific_df['Payload Mass (kg)'] >= payload_slider[0])
                                    & (specific_df['Payload Mass (kg)'] <= payload_slider[1])]
        scatterplot = go.Figure(data=go.Scatter(x=filtered_data["Payload Mass (kg)"], y=filtered_data["class"],
                                                mode='markers', marker=dict(color="Booster Version Category")))
        scatterplot.update_layout(title='Correlation between payload and launch success',
                                  xaxis_title='Payload Mass (kg)', yaxis_title='Class')
        return scatterplot

# Run the app
if __name__ == '__main__':
    app.run_server()
