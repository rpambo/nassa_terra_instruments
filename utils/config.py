# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Meteomatics API Configuration
METEOMATICS_USERNAME = os.getenv('METEOMATICS_USERNAME', 'pambo_rafael')
METEOMATICS_PASSWORD = os.getenv('METEOMATICS_PASSWORD', '4gv01w9dlN8Uc5Rp82F3')

# App Configuration
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
PORT = int(os.getenv('PORT', '8050'))
HOST = os.getenv('HOST', '127.0.0.1')

# Map Configuration
DEFAULT_CENTER = [30.0, 100.0]
DEFAULT_ZOOM = 3