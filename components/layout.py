# components/layout.py
import dash_leaflet as dl
from dash import html, dcc
import dash_bootstrap_components as dbc
from data.regions import REGIONS_DATA, REGION_DESCRIPTIONS
from utils.helpers import make_modis_url

def create_layout():
    """Create the main application layout"""
    
    # Initial MODIS layer
    modis_layer = dl.TileLayer(
        url=make_modis_url(2024),
        attribution="NASA GIBS - MODIS",
        id="modis-layer"
    )

    # Contours layer
    contours_layer = dl.TileLayer(
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri",
        id="contours"
    )

    return html.Div([
        # Search bar in top right corner
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🔍 Cities for Analysis", style={'color': 'white', 'marginBottom': '15px'}),
                    dcc.Dropdown(
                        id='region-search',
                        options=[{'label': region, 'value': region} for region in REGIONS_DATA.keys()],
                        value='Beijing China',
                        placeholder="Select a city...",
                        style={'width': '220px', 'color': 'black'}
                    ),
                    html.Div(id='location-info', style={'color': 'white', 'fontSize': '11px', 'textAlign': 'center', 'marginTop': '10px'})
                ])
            ], style={'backgroundColor': 'rgba(44, 62, 80, 0.95)', 'border': '1px solid #3498db', 'width': '270px'})
        ], style={'position': 'absolute', 'top': '20px', 'right': '20px', 'zIndex': 1000}),

        # Controls in bottom right corner
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H6("⚙️ Controls", style={'color': 'white', 'marginBottom': '15px'}),
                    html.Label("Year:", style={'color': 'white', 'fontSize': '12px'}),
                    dcc.Slider(id="year", min=2016, max=2024, step=1, value=2024,
                               marks={y: str(y) for y in range(2016, 2025, 2)},
                               tooltip={"placement": 'bottom', "always_visible": True}),
                    
                    html.Hr(style={'borderColor': '#3498db', 'margin': '10px 0'}),
                    
                    html.Label("🛰️ Instrument Combination:", style={'color': 'white', 'fontSize': '12px', 'marginBottom': '10px'}),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Checklist(
                                id='instrument-combination',
                                options=[
                                    {'label': ' MODIS', 'value': 'modis'},
                                    {'label': ' MOPITT', 'value': 'mopitt'}
                                ],
                                value=['modis', 'mopitt'],
                                style={'color': 'white', 'fontSize': '11px'}
                            )
                        ], width=12)
                    ], style={'marginBottom': '10px'}),
                    
                    html.Div(id='combination-indicator', 
                            style={'color': '#3498db', 'fontSize': '10px', 'textAlign': 'center', 
                                  'marginBottom': '10px', 'fontWeight': 'bold'}),
                    
                    html.Hr(style={'borderColor': '#3498db', 'margin': '10px 0'}),
                    dbc.Row([
                        dbc.Col(dbc.Button("▶️ Play", id='play-animation', color='success', size='sm', style={'width': '100%'}), width=6),
                        dbc.Col(dbc.Button("⏸️ Pause", id='pause-animation', color='warning', size='sm', style={'width': '100%'}), width=6),
                    ], style={'marginBottom': '10px'}),
                    html.Div(id='animation-status', style={'color': '#3498db', 'fontSize': '10px', 'textAlign': 'center', 'marginTop': '5px'}),
                    html.Hr(style={'borderColor': '#3498db', 'margin': '10px 0'}),
                    
                    html.Label("View:", style={'color': 'white', 'fontSize': '12px'}),
                    dcc.RadioItems(id='view-mode', options=[
                        {'label': ' 🛰️ Satellite', 'value': 'satellite-only'},
                        {'label': ' 📐 With borders', 'value': 'with-borders'}
                    ], value='with-borders', style={'color': 'white', 'fontSize': '11px'})
                ])
            ], style={'backgroundColor': 'rgba(44, 62, 80, 0.95)', 'border': '1px solid #3498db', 'width': '280px', 'height': '380px'})
        ], style={'position': 'absolute', 'bottom': '20px', 'right': '20px', 'zIndex': 1000}),

        # Meteorological data on the left
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H5("📊 Meteorological Data (2016-2024)", 
                               style={'color': 'white', 'marginBottom': '15px', 'textAlign': 'center', 'display': 'inline-block'}),
                        dbc.Button(
                            "📈 Hide Chart", 
                            id="toggle-chart-button", 
                            color="primary", 
                            size="sm",
                            style={
                                'float': 'right', 
                                'marginLeft': '10px',
                                'backgroundColor': '#3498db',
                                'borderColor': '#3498db',
                                'fontSize': '10px'
                            }
                        )
                    ], style={'marginBottom': '15px'}),
                    
                    # 3 HORIZONTAL BOXES
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(
                                        id='temperature-graph',
                                        config={'displayModeBar': False},
                                        style={'height': '100px'}
                                    )
                                ])
                            ], style={'backgroundColor': 'rgba(52, 152, 219, 0.1)', 'border': '1px solid #3498db', 'height': '130px'})
                        ], width=4),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(
                                        id='precipitation-graph',
                                        config={'displayModeBar': False},
                                        style={'height': '100px'}
                                    )
                                ])
                            ], style={'backgroundColor': 'rgba(52, 152, 219, 0.1)', 'border': '1px solid #3498db', 'height': '130px'})
                        ], width=4),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(
                                        id='co-graph',
                                        config={'displayModeBar': False},
                                        style={'height': '100px'}
                                    )
                                ])
                            ], style={'backgroundColor': 'rgba(52, 152, 219, 0.1)', 'border': '1px solid #3498db', 'height': '130px'})
                        ], width=4)
                    ])
                ])
            ], style={'backgroundColor': 'rgba(44, 62, 80, 0.95)',
                      'border': '1px solid #3498db',
                      'width': '800px',
                      'height': '200px',
                      'overflowY': 'auto'})
        ], style={'position': 'absolute', 'top': '20px', 'left': '20px', 'zIndex': 1000}),

        # COMPARATIVE CHART
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📈 Comparative Chart", 
                           style={'color': 'white', 'marginBottom': '15px', 'textAlign': 'center'}),
                    
                    dcc.Graph(
                        id='comparison-chart',
                        config={'displayModeBar': True},
                        style={'height': '250px'}
                    )
                ])
            ], style={'backgroundColor': 'rgba(44, 62, 80, 0.95)',
                      'border': '1px solid #e67e22',
                      'width': '800px',
                      'height': '320px'})
        ], style={'position': 'absolute', 'top': '240px', 'left': '20px', 'zIndex': 1000}, id='comparison-chart-container'),

        # Main map
        dl.Map(center=[35.0, 105.0], zoom=3, children=[modis_layer, contours_layer],
               style={"width": "100%", "height": "100vh"}, id="map"),
        
        # Storage components
        dcc.Interval(id='animation-interval', interval=2000, n_intervals=0),
        dcc.Store(id='animation-store', data={'is_playing': False, 'current_year': 2024}),
        dcc.Store(id='chart-visibility-store', data={'chart_visible': True})
    ], style={'backgroundColor': '#1a1a1a', 'margin': '0', 'padding': '0', 'height': '100vh', 'position': 'relative'})