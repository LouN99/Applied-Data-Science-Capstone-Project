# Import required libraries
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc  # Updated import statements
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
launch_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = launch_df['Payload Mass (kg)'].max()
min_payload = launch_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)  # Updated for Dash v2

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'ALL SITES', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={0: '0', 2500: '2500', 5000: '5000',
               7500: '7500', 10000: '10000'}
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(launch_site):
    if launch_site == 'ALL':  # Updated comparison
        # Calculate total successful launches per site
        success_counts = launch_df[launch_df['class'] == 1].groupby('Launch Site').size().reset_index(name='counts')
        fig = px.pie(
            success_counts,
            names='Launch Site',
            values='counts',
            title='Total Successful Launches by Site'
        )
    else:
        # Filter data for the selected site
        filtered_df = launch_df[launch_df['Launch Site'] == launch_site]
        # Calculate counts of success vs failure
        success_failure_counts = filtered_df['class'].value_counts().reset_index()
        success_failure_counts.columns = ['class', 'count']
        # Map class values to labels
        success_failure_counts['class'] = success_failure_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            success_failure_counts,
            names='class',
            values='count',
            title=f'Total Launch Outcomes for {launch_site}'
        )
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_payload_chart(launch_site, payload_range):
    low, high = payload_range
    mask = launch_df['Payload Mass (kg)'].between(low, high)

    if launch_site == 'ALL':
        filtered_df = launch_df[mask]
        title = 'Correlation Between Payload and Success for All Sites'
    else:
        filtered_df = launch_df[(launch_df['Launch Site'] == launch_site) & mask]
        title = f'Correlation Between Payload and Success for {launch_site}'

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=['Launch Site'],
        title=title,
        labels={'class': 'Launch Outcome'},
        category_orders={'class': [0, 1]},
        # Optionally, map class to more descriptive labels
    )

    # Update y-axis to show descriptive labels
    fig.update_yaxes(tickvals=[0, 1], ticktext=['Failure', 'Success'])

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
    
