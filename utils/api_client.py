# utils/api_client.py
import meteomatics.api as api
from datetime import datetime, timedelta
from utils.config import METEOMATICS_USERNAME, METEOMATICS_PASSWORD

def get_meteomatics_data(lat, lon, year, include_co=False):
    """Get meteorological data from Meteomatics API"""
    try:
        coordinates = [(lat, lon)]
        
        base_parameters = [
            't_2m:C',           # Temperature at 2m in Celsius
            'precip_1h:mm',     # Precipitation in last hour
            'wind_speed_10m:ms' # Wind speed at 10m
        ]
        
        co_parameters = ['co:ugm3'] if include_co else []
        
        model = 'mix'
        current_year = datetime.now().year
        
        if year == current_year:
            startdate = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
            enddate = startdate + timedelta(hours=1)
            parameters = base_parameters + co_parameters
        else:
            startdate = datetime(year, 6, 15, 12, 0, 0)
            enddate = startdate + timedelta(hours=1)
            parameters = base_parameters + co_parameters
        
        interval = timedelta(hours=1)

        print(f"Getting Meteomatics data for ({lat}, {lon}) in year {year}")
        print(f"Include CO: {include_co}")
        
        df = api.query_time_series(coordinates, startdate, enddate, interval, 
                                 parameters, METEOMATICS_USERNAME, METEOMATICS_PASSWORD, 
                                 model=model)
        
        if not df.empty:
            first_row = df.iloc[0]
            parsed_data = {}
            
            for param in parameters:
                if param in df.columns:
                    parsed_data[param] = first_row[param]
                else:
                    parsed_data[param] = 'N/A'
            
            parsed_data['co_available'] = 'co:ugm3' in parameters
            return parsed_data
        else:
            print("No data returned by Meteomatics API")
            return None
            
    except Exception as e:
        print(f"Error accessing Meteomatics API: {e}")
        return None