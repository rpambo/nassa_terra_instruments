# utils/helpers.py
from datetime import datetime, timedelta

def make_modis_url(year):
    date = f"{year}-06-15"
    return f"https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/{date}/GoogleMapsCompatible_Level9/{{z}}/{{y}}/{{x}}.jpg"

def make_mopitt_url(year):
    """Generate URL for MOPITT data (Carbon Monoxide) based on year"""
    current_year = datetime.now().year
    if year == current_year:
        target_date = datetime.now() - timedelta(days=60)
        date = target_date.strftime("%Y-%m-15")
    else:
        date = f"{year}-06-15"
    
    print(f"MOPITT URL for year {year}: using date {date}")
    return f"https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MOPITT_CO_Monthly_Total_Column_Day/default/{date}/GoogleMapsCompatible_Level6/{{z}}/{{y}}/{{x}}.png"