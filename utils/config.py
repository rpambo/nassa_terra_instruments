# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Meteomatics API Configuration
METEOMATICS_USERNAME = os.getenv('METEOMATICS_USERNAME', '')
METEOMATICS_PASSWORD = os.getenv('METEOMATICS_PASSWORD', '')

# App Configuration
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
PORT = int(os.getenv('PORT', '8050'))
HOST = os.getenv('HOST', '0.0.0.0')

# Map Configuration
DEFAULT_CENTER = [30.0, 100.0]
DEFAULT_ZOOM = 3