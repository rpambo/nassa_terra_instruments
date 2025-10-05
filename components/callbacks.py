# components/callbacks.py
from dash import Output, Input, State, callback_context, no_update
import dash_leaflet as dl
from data.regions import REGIONS_DATA, REGION_DESCRIPTIONS
from utils.api_client import get_meteomatics_data
from utils.helpers import make_modis_url, make_mopitt_url
from components.graphs import (
    create_temperature_gauge_horizontal, 
    create_precipitation_bar_horizontal,
    create_co_gauge_horizontal,
    create_empty_gauge_horizontal,
    create_comparison_chart,
    create_empty_comparison_chart
)

# Historical data storage (could be moved to a database)
historical_data = {}

def get_weather_data(region_name, year, include_co=False):
    """Get meteorological data from Meteomatics API"""
    try:
        region = REGIONS_DATA.get(region_name, REGIONS_DATA['Beijing China'])
        lat, lon = region['lat'], region['lon']
        
        print(f"Getting data for {region_name} ({lat}, {lon}) in year {year}")
        print(f"Include CO in data: {include_co}")
        
        weather_data = get_meteomatics_data(lat, lon, year, include_co)
        
        if not weather_data:
            return {
                'error': True,
                'message': f'Error getting data from Meteomatics API for year {year}'
            }
        
        temperature = weather_data.get('t_2m:C', 'N/A')
        precipitation = weather_data.get('precip_1h:mm', 'N/A')
        wind_speed = weather_data.get('wind_speed_10m:ms', 'N/A')
        co_concentration = weather_data.get('co:ugm3', 'N/A') if include_co else None
        
        result = {
            'temperature': round(temperature, 1) if temperature != 'N/A' else None,
            'precipitation': round(precipitation * 24, 1) if precipitation != 'N/A' else None,
            'wind_speed': round(wind_speed, 1) if wind_speed != 'N/A' else None,
            'co_concentration': round(co_concentration, 2) if co_concentration != 'N/A' and include_co else None,
            'region': region_name,
            'coordinates': f"Lat: {lat:.4f}, Lon: {lon:.4f}",
            'year': year,
            'error': False
        }
        
        # Store historical data for comparative chart
        if region_name not in historical_data:
            historical_data[region_name] = {}
        
        historical_data[region_name][year] = {
            'temperature': result['temperature'],
            'precipitation': result['precipitation'],
            'co_concentration': result['co_concentration']
        }
        
        return result
        
    except Exception as e:
        print(f"Error getting meteorological data: {e}")
        return {
            'error': True,
            'message': f'Error: {str(e)}'
        }

def register_callbacks(app):
    """Register all callbacks in the application"""
    
    # Callback to show/hide chart
    @app.callback(
        [Output('comparison-chart-container', 'style'),
         Output('toggle-chart-button', 'children')],
        [Input('toggle-chart-button', 'n_clicks')],
        [State('chart-visibility-store', 'data')]
    )
    def toggle_chart(n_clicks, visibility_data):
        if n_clicks is None:
            return {
                'position': 'absolute',
                'top': '240px',
                'left': '20px',
                'zIndex': 1000,
                'transition': 'all 0.3s ease-in-out'
            }, "📈 Hide Chart"
        
        chart_visible = not visibility_data['chart_visible']
        
        if chart_visible:
            return {
                'position': 'absolute',
                'top': '240px',
                'left': '20px',
                'zIndex': 1000,
                'transition': 'all 0.3s ease-in-out'
            }, "📈 Hide Chart"
        else:
            return {
                'position': 'absolute',
                'top': '240px',
                'left': '-850px',
                'zIndex': 1000,
                'transition': 'all 0.3s ease-in-out'
            }, "📈 Show Chart"

    # Callback to update visibility store
    @app.callback(
        Output('chart-visibility-store', 'data'),
        [Input('toggle-chart-button', 'n_clicks')],
        [State('chart-visibility-store', 'data')]
    )
    def update_visibility_store(n_clicks, visibility_data):
        if n_clicks is None:
            return {'chart_visible': True}
        
        return {'chart_visible': not visibility_data['chart_visible']}

    # Callback to update map
    @app.callback(
        [Output("map", "children"),
         Output("combination-indicator", "children")],
        [Input("view-mode", "value"),
         Input("year", "value"),
         Input("instrument-combination", "value")]
    )
    def update_view_mode(mode, year, instrument_combination):
        print(f"Updating map - Combination: {instrument_combination}, Year: {year}")
        
        layers = []
        instrument_names = []
        
        if 'modis' in instrument_combination:
            modis_url = make_modis_url(year)
            modis_layer = dl.TileLayer(url=modis_url, attribution="NASA GIBS - MODIS Terra")
            layers.append(modis_layer)
            instrument_names.append("MODIS")
        
        if 'mopitt' in instrument_combination:
            mopitt_url = make_mopitt_url(year)
            mopitt_layer = dl.TileLayer(
                url=mopitt_url, 
                attribution="NASA GIBS - MOPITT/Terra",
                opacity=0.6
            )
            layers.append(mopitt_layer)
            instrument_names.append("MOPITT")
        
        if not layers:
            modis_url = make_modis_url(year)
            modis_layer = dl.TileLayer(url=modis_url, attribution="NASA GIBS - MODIS Terra")
            layers.append(modis_layer)
            instrument_names.append("MODIS")
        
        if mode == 'with-borders':
            contours = dl.TileLayer(
                url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
                attribution="Esri"
            )
            layers.append(contours)
        
        if len(instrument_names) == 1:
            indicator_text = f"📡 Instrument: {instrument_names[0]}"
        else:
            indicator_text = f"🛰️ Combination: {', '.join(instrument_names)}"
        
        return layers, indicator_text

    # Callback to update location
    @app.callback(
        [Output("map", "viewport"), Output("location-info", "children")],
        Input("region-search", "value")
    )
    def update_location(region):
        if region:
            region_data = REGIONS_DATA[region]
            info = f"📍 {region} | {REGION_DESCRIPTIONS.get(region, '')}"
            return {'center': [region_data['lat'], region_data['lon']], 'zoom': region_data['zoom']}, info
        return no_update, ""

    # Callbacks for animation
    @app.callback(
        [Output('animation-store', 'data'),
         Output('animation-status', 'children')],
        [Input('play-animation', 'n_clicks'),
         Input('pause-animation', 'n_clicks')],
        [State('animation-store', 'data')]
    )
    def control_animation(play_clicks, pause_clicks, data):
        ctx = callback_context
        if not ctx.triggered:
            return data, "⏹️ Stopped"
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == 'play-animation':
            data['is_playing'] = True
            status = f"▶️ Playing... Year: {data['current_year']}"
            return data, status
        
        elif trigger_id == 'pause-animation':
            data['is_playing'] = False
            status = f"⏸️ Paused - Year: {data['current_year']}"
            return data, status
        
        return data, "⏹️ Stopped"

    @app.callback(
        [Output('year', 'value'),
         Output('animation-store', 'data', allow_duplicate=True)],
        [Input('animation-interval', 'n_intervals')],
        [State('animation-store', 'data')],
        prevent_initial_call=True
    )
    def update_animation_frame(n_intervals, data):
        if data['is_playing']:
            current_year = data['current_year'] + 1
            if current_year > 2024:
                current_year = 2016
            
            data['current_year'] = current_year
            return current_year, data
        
        return no_update, data

    # Main callback to update charts
    @app.callback(
        [Output('temperature-graph', 'figure'),
         Output('precipitation-graph', 'figure'),
         Output('co-graph', 'figure'),
         Output('comparison-chart', 'figure')],
        [Input("region-search", "value"), 
         Input("year", "value"),
         Input("instrument-combination", "value")]
    )
    def update_weather_graphs(region, year, instrument_combination):
        if not region:
            empty_fig = create_empty_gauge_horizontal("", "Select region")
            return empty_fig, empty_fig, empty_fig, create_empty_comparison_chart()
        
        include_co = 'mopitt' in instrument_combination
        print(f"Updating data - Include CO: {include_co}")
        
        data = get_weather_data(region, year, include_co)
        
        if data.get('error'):
            error_fig = create_empty_gauge_horizontal("Error", "Data unavailable")
            return error_fig, error_fig, error_fig, create_empty_comparison_chart()
        
        temp_fig = create_temperature_gauge_horizontal(data['temperature'])
        precip_fig = create_precipitation_bar_horizontal(data['precipitation'])
        
        if include_co:
            co_fig = create_co_gauge_horizontal(data['co_concentration'])
        else:
            co_fig = create_empty_gauge_horizontal("🌫️ CO", "Select MOPITT")
        
        comparison_fig = create_comparison_chart(region, historical_data)
        
        return temp_fig, precip_fig, co_fig, comparison_fig