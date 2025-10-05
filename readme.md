# Meteorology Dashboard with Satellite Data

Interactive dashboard for visualizing meteorological and pollution data using Meteomatics API and NASA satellite imagery.

## Features

- **Real-time Data**: Temperature, precipitation, and wind speed
- **CO Monitoring**: Carbon monoxide data via MOPITT
- **Satellite Imagery**: MODIS and MOPITT from NASA
- **Comparative Analysis**: Historical data from 2016-2024
- **Interactive Interface**: Interactive map with controls

## Available Cities

- Beijing, China
- Shanghai, China
- Delhi, India

## 🛰️ Instruments

- **MODIS**: True reflectance satellite imagery
- **MOPITT**: Carbon monoxide data

## 🔧 Project Structure

meteomatics-dashboard/
├── app.py                 # Main application
├── components/           # Dash components
├── utils/               # Utilities and configurations
├── data/               # Data and configurations
└── requirements.txt    # Dependencies

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rpambo/meteomatics-dashboard.git
cd meteomatics-dashboard
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your Meteomatics API credentials
```

4. Run the application:

```bash
python app.py
```

## 📝 License

This project is licensed under the MIT License.

