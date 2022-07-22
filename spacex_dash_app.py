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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                               
                                dcc.Dropdown(id='site-dropdown',
                                 options=[
                                {'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label':'KSC LC-39A','value': 'KSC LC-39A'},
                                 {'label':'CCAFS SLC-40','value': 'CCAFS SLC-40'}
                                 ],
                                 value='ALL',
                                 placeholder="Select a Launch Site here",
                                 searchable=True
                                 ),
                                html.Br(),

                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'},
                                                value=[0,10000]),
                              
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total count of class')
        return fig
    else:
        Bool=spacex_df['Launch Site']==entered_site 
        filtered_df = spacex_df[Bool]
        class1=list(1 for i in range (filtered_df.shape[0]) )
        filtered_df['class1']=class1
        fig = px.pie(filtered_df, values='class1', 
        names='class', 
        title='Total Success Launches for Site')
        return fig

    
    
   
@app.callback(
          Output(component_id='success-payload-scatter-chart', component_property='figure'),
          [Input(component_id='site-dropdown', component_property='value'), 
          Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site,payload_mass):
    lower,upper=payload_mass
    Bool=(spacex_df['Payload Mass (kg)']<upper) & (spacex_df['Payload Mass (kg)']> lower)
    filtered_df=spacex_df[Bool]
    if entered_site=='ALL':
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for all Sites')
        return fig


    else:
        Bool= filtered_df['Launch Site']==entered_site
        filtered_df=filtered_df[Bool]
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for selected Site')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
