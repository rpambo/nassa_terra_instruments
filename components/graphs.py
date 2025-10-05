# components/graphs.py
import plotly.graph_objects as go
import plotly.express as px

def create_temperature_gauge_horizontal(temp_value):
    """Create horizontal gauge chart for temperature"""
    if temp_value == 'N/A' or temp_value is None:
        return create_empty_gauge_horizontal("🌡️ Temperature", "N/A")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = temp_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "🌡️ Temperature (°C)", 'font': {'size': 10, 'color': 'white'}},
        gauge = {
            'axis': {'range': [-20, 50], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white', 'size': 8}},
            'bar': {'color': "#e67e22"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1,
            'bordercolor': "#3498db",
            'steps': [
                {'range': [-20, 0], 'color': '#3498db'},
                {'range': [0, 10], 'color': '#2980b9'},
                {'range': [10, 20], 'color': '#27ae60'},
                {'range': [20, 30], 'color': '#e67e22'},
                {'range': [30, 50], 'color': '#e74c3c'}],
            'threshold': {
                'line': {'color': "white", 'width': 2},
                'thickness': 0.6,
                'value': temp_value}}))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Arial"},
        height=120,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def create_precipitation_bar_horizontal(precip_value):
    """Create horizontal bar chart for precipitation"""
    if precip_value == 'N/A' or precip_value is None:
        return create_empty_bar_horizontal("🌧️ Precipitation", "N/A")
    
    fig = go.Figure(go.Bar(
        x=[precip_value],
        y=[''],
        orientation='h',
        marker_color='#3498db',
        text=[f"{precip_value} mm"],
        textposition='auto',
        hovertemplate=f"Precipitation: {precip_value} mm<extra></extra>"
    ))
    
    fig.update_layout(
        title={'text': "🌧️ Precipitation (mm)", 'font': {'size': 10, 'color': 'white'}, 'x': 0.5},
        xaxis={
            'range': [0, 300],
            'showgrid': True,
            'gridcolor': '#34495e',
            'color': 'white',
            'tickfont': {'color': 'white', 'size': 8},
            'title': ''
        },
        yaxis={'visible': False},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=120,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False
    )
    
    return fig

def create_co_gauge_horizontal(co_value):
    """Create horizontal gauge chart for CO concentration"""
    if co_value == 'N/A' or co_value is None:
        return create_empty_gauge_horizontal("🌫️ CO", "N/A")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = co_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "🌫️ CO (μg/m³)", 'font': {'size': 9, 'color': 'white'}},
        gauge = {
            'axis': {'range': [0, 200], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white', 'size': 8}},
            'bar': {'color': "#e67e22"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1,
            'bordercolor': "#e67e22",
            'steps': [
                {'range': [0, 50], 'color': '#27ae60'},
                {'range': [50, 100], 'color': '#f1c40f'},
                {'range': [100, 150], 'color': '#e67e22'},
                {'range': [150, 200], 'color': '#e74c3c'}],
            'threshold': {
                'line': {'color': "white", 'width': 2},
                'thickness': 0.6,
                'value': co_value}}))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Arial"},
        height=120,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def create_empty_gauge_horizontal(title, message):
    """Create empty horizontal gauge for unavailable data"""
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = 0,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{title}<br>{message}", 'font': {'size': 12, 'color': '#bdc3c7'}},
        number = {'font': {'color': '#bdc3c7', 'size': 10}}
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=120,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def create_empty_bar_horizontal(title, message):
    """Create empty horizontal bar chart for unavailable data"""
    fig = go.Figure()
    fig.update_layout(
        title={'text': f"{title}<br>{message}", 'font': {'size': 12, 'color': '#bdc3c7'}, 'x': 0.5},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=120,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis={'visible': False},
        yaxis={'visible': False}
    )
    return fig

def create_comparison_chart(region_name, historical_data):
    """Create comparative chart with historical data"""
    if region_name not in historical_data or not historical_data[region_name]:
        return create_empty_comparison_chart()
    
    data = historical_data[region_name]
    years = sorted(data.keys())
    
    temperatures = []
    precipitations = []
    co_concentrations = []
    valid_years = []
    
    for year in years:
        if data[year]['temperature'] is not None:
            temperatures.append(data[year]['temperature'])
            precipitations.append(data[year]['precipitation'] if data[year]['precipitation'] is not None else 0)
            co_concentrations.append(data[year]['co_concentration'] if data[year]['co_concentration'] is not None else 0)
            valid_years.append(year)
    
    if not valid_years:
        return create_empty_comparison_chart()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=valid_years, y=temperatures,
        mode='lines+markers',
        name='Temperature (°C)',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8, color='#e74c3c'),
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        x=valid_years, y=precipitations,
        name='Precipitation (mm)',
        marker_color='#3498db',
        opacity=0.6,
        yaxis='y'
    ))
    
    has_co_data = any(co > 0 for co in co_concentrations)
    if has_co_data:
        fig.add_trace(go.Scatter(
            x=valid_years, y=co_concentrations,
            mode='lines+markers',
            name='CO (μg/m³)',
            line=dict(color='#e67e22', width=3, dash='dot'),
            marker=dict(size=8, color='#e67e22'),
            yaxis='y2'
        ))
    
    layout_config = {
        'title': {
            'text': f'📈 Data Evolution - {region_name} (2016-2024)',
            'font': {'size': 14, 'color': 'white', 'family': 'Arial'},
            'x': 0.2
        },
        'xaxis': dict(
            title='Year',
            tickmode='linear',
            tick0=2016,
            dtick=1,
            color='white',
            gridcolor='#34495e',
            title_font=dict(color='white')
        ),
        'yaxis': dict(
            title='Temperature (°C) / Precipitation (mm)',
            title_font=dict(color='#e74c3c'),
            tickfont=dict(color='#e74c3c'),
            gridcolor='#34495e',
            zerolinecolor='#34495e'
        ),
        'legend': dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'height': 250,
        'margin': dict(l=50, r=50, t=60, b=50),
        'hovermode': 'x unified'
    }
    
    if has_co_data:
        layout_config['yaxis2'] = dict(
            title='CO (μg/m³)',
            title_font=dict(color='#e67e22'),
            tickfont=dict(color='#e67e22'),
            overlaying='y',
            side='right',
            gridcolor='#34495e'
        )
    
    fig.update_layout(**layout_config)
    return fig

def create_empty_comparison_chart():
    """Create empty comparative chart"""
    fig = go.Figure()
    fig.update_layout(
        title={
            'text': '📈 Comparative Chart',
            'font': {'size': 14, 'color': 'white'},
            'x': 0.5
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=250,
        margin=dict(l=50, r=50, t=60, b=50),
        xaxis={'visible': False},
        yaxis={'visible': False},
        annotations=[{
            'text': 'Navigate through years to generate comparative data',
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.5,
            'y': 0.5,
            'showarrow': False,
            'font': {'size': 12, 'color': '#bdc3c7'}
        }]
    )
    return fig