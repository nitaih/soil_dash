from click import style
import pandas as pd
import geopandas as gpd
from shapely import wkt
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash import no_update

data = pd.read_csv(r'C:\Users\nitaih\OneDrive - InnoValley Ltd\Dash_creations\soil_tests_database.csv')

crop_list = data['crop'].unique()
year_list = data['year'].unique()
location_list = data['location'].unique()
test_list = list(data.columns[6:10])
depth_list = data['depth'].unique()
treatment_list = data['treatment'].unique()


def soil_boxplot(df, treatment_list, meas, location):
    rows = [1,1,1,2,2,2,3,3,3]
    columns = [1,2,3,1,2,3,1,2,3]

    # setting axis range per measurement
    if meas == 'EC (dS/m)':
        rng = [0, 5]
    elif meas == 'Cl (mg/l)':
        rng = [0, 1010]
    elif meas == 'SAR':
        rng = [0, 10]
    elif meas == 'CaCO3 (%)':
        rng = [0, 70]

    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=treatment_list)
    for i,t in enumerate(treatment_list):
        dft = df[df['treatment']==t]

        fig.add_trace(go.Box(x=dft[meas].loc[dft['depth']=='60-90'],name='60-90',boxpoints='all',fillcolor='rgba(7,123,239,0.45)',line=dict(color='rgba(7,123,239,1)',width=1)),row=rows[i],col=columns[i]) # ,fillcolor='rgba(7,179,239,0.6)',line=dict(color='rgba(7,179,239,1)',width=1)
        fig.add_trace(go.Box(x=dft[meas].loc[dft['depth']=='30-60'],name='30-60',boxpoints='all',fillcolor='rgba(7,123,239,0.45)',line=dict(color='rgba(7,123,239,1)',width=1)),row=rows[i],col=columns[i])
        fig.add_trace(go.Box(x=dft[meas].loc[dft['depth']=='0-30'],name='0-30',boxpoints='all',fillcolor='rgba(7,123,239,0.45)',line=dict(color='rgba(7,123,239,1)',width=1)),row=rows[i],col=columns[i])
        if i == 6:
            fig.update_layout(yaxis_title="depth (cm)")
        fig.update_xaxes(range = rng)

    fig.update_layout(showlegend=False)
    fig.update_layout(title = '{0} soil {1}'.format(location, meas), height=600)
    return fig

# Create a dash application
app = Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True
app.layout = html.Div(children = [
    html.H1('Water Salinity Project - Soil tests dashboard', style={'textAlign':'left','color':'#503D36','font-size':30}),
    html.Div([
        # add next division for year selector
        html.Div([
            html.Div(
                [
                    html.H2('Select a Year', style={'margin-right': '2em', 'font-size': '15px'}),
                    ]
            ),
            dcc.Dropdown(id='input-year', 
            options=[{'label':i,'value':i} for i in year_list],
            value=2022,
            placeholder = 'Select a Year',
            style = {'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
            ], style = {'display': 'flex'}),
            # add next division for crop selector
            html.Div([
                html.Div(
                    [
                        html.H2('Select a Crop', style={'margin-right': '2em', 'font-size': '15px'})
                        ]
                        ),
                        dcc.Dropdown(id= 'input-crop', 
                        options = [{'label':j, 'value':j} for j in crop_list],
                        value = 'mango',
                        placeholder='Select a Crop',
                        style={'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
                        ], style = {'display': 'flex'}),
                        # add next division for location selector
                        html.Div([
                            html.Div(
                                [
                                    html.H2('Select Location', style={'margin-right': '2em', 'font-size': '15px'})
                                    ]
                                    ),
                                    dcc.Dropdown(id= 'input-location', 
                                    options = [{'label':k, 'value':k} for k in location_list],
                                    value = 'merav',
                                    placeholder='Select Location',
                                    style={'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
                                    ], style = {'display': 'flex'}),
                                    ]),
                                    
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                html.Div([
                                                    html.H2('Select measuremnt', style={'margin-right': '2em', 'font-size': '15px'})
                                                    ]
                                                ),
                                                dcc.Dropdown(id= 'input-meas', 
                                                    options = [{'label':k, 'value':k} for k in test_list],
                                                    value = 'EC (dS/m)',
                                                    placeholder='Select measurement',
                                                    style={'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
                                            ], style = {'display': 'flex'}),
                                            html.Div([ ], id='plot1'),
                                            ], style={'width':'60%'}),
                                        html.Div([
                                            html.H2('soil test Map', style={'margin-right': '2em', 'font-size': '15px'}),
                                            html.Div([
                                                html.Div([
                                                    html.H2('Select depth', style={'margin-right': '2em', 'font-size': '15px'})
                                                    ]
                                                ),
                                                dcc.Dropdown(id= 'input-depth', 
                                                    options = [{'label':k, 'value':k} for k in depth_list],
                                                    value = '0-30',
                                                    placeholder='Select depth',
                                                    style={'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
                                            ], style = {'display': 'flex'}),
                                            html.Div([ ], id='plot2'),
                                            ] , style={'width':'40%'}),
                                            ], style = {'display': 'flex'}), 
                                        ])
                                    

@app.callback([
    Output(component_id='plot1', component_property='children'), 
    Output(component_id='plot2', component_property='children')],
    [
        Input(component_id='input-year', component_property='value'),
        Input(component_id='input-crop', component_property='value'),
        Input(component_id='input-location', component_property='value'),
        Input(component_id='input-meas', component_property='value'),
        Input(component_id='input-depth', component_property='value')],
        [
            State(component_id="plot1", component_property='children'), 
            State(component_id="plot2", component_property="children")])
# Add computation to callback function and return graph
def get_graph(year, crop, location, meas, depth, children1, children2):
    # filter year
    dfy = data[data['year'] == year]
    # filter crop
    dfc = dfy[dfy['crop'] == crop]
    # filter location
    dfl = dfc[dfc['location'] == location]
    # filter depth
    dfd = dfl[dfl['depth'] == depth]
    # if crop == 'onion':
    #     units = 'Large/Total Ratio'
    # else: units = 'g'

    if crop == 'dates':
        if location == 'merav':
            coord = [32.45229, 35.52110]
            zoom = 17
        elif location == 'havat eden':
            coord = [32.46669, 35.49053]
            zoom = 17
    elif crop == 'mango':
        if location == 'merav':
            coord = [32.45752, 35.45842] 
            zoom = 18
        elif location == 'nir david':
            coord = [32.50266, 35.44758]
            zoom = 17.5
    elif crop == 'onion':
        coord = [32.46820, 35.48803]
        zoom = 17.5

    dfd['geometry'] = dfd['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(dfd, crs='epsg:4326')
    
    box_fig = soil_boxplot(dfl, treatment_list, meas, location)
    # rows = [1,1,1,2,2,2,3,3,3]
    # columns = [1,2,3,1,2,3,1,2,3]
    # fig = make_subplots(
    #     rows=3, cols=3,
    #     subplot_titles=treatment_list)
    # for i,t in enumerate(treatment_list):
    #     dft = dfl[dfl['treatment']==t]

    #     fig.add_trace(go.Box(x=dft[meas].loc[dft['depth']=='60-90'],name='60-90',boxpoints='all',fillcolor='rgba(7,123,239,0.45)',line=dict(color='rgba(7,123,239,1)',width=1)),row=rows[i],col=columns[i]) # ,fillcolor='rgba(7,179,239,0.6)',line=dict(color='rgba(7,179,239,1)',width=1)
    #     fig.add_trace(go.Box(x=dft[meas].loc[dft['depth']=='30-60'],name='30-60',boxpoints='all',fillcolor='rgba(7,123,239,0.45)',line=dict(color='rgba(7,123,239,1)',width=1)),row=rows[i],col=columns[i])
    #     fig.add_trace(go.Box(x=dft[meas].loc[dft['depth']=='0-30'],name='0-30',boxpoints='all',fillcolor='rgba(7,123,239,0.45)',line=dict(color='rgba(7,123,239,1)',width=1)),row=rows[i],col=columns[i])
    #     if i == 6:
    #         fig.update_layout(xaxis_title=meas, yaxis_title="depth (cm)")
    #     fig.update_xaxes(range = [0,10])
        
    # fig.update_layout(showlegend=False)
    # fig.update_layout(title = '{0} soil {1}'.format(location, meas)) 
       
    map_fig = px.choropleth_mapbox(gdf,
                           geojson=gdf.geometry,
                           locations=gdf.index,
                           color_continuous_scale = 'YlOrBr',
                           hover_name="treatment",
                        #    hover_data=["salinity", "water amount"],
                           color=meas,
                           center={"lat": coord[0], "lon": coord[1]}, #35.44758,32.50266
                        #    mapbox_style="open-street-map",
                           zoom=zoom,
                           )

    map_fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "Google Hybrid",
                "source": [
                    "http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}"
                ]
            }
        ])
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return [dcc.Graph(figure=box_fig), dcc.Graph(figure=map_fig)]
# Run the app
if __name__ == '__main__':
    app.run_server()