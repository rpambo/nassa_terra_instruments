# app.py
import dash
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings('ignore')

from utils.config import DEBUG, PORT, HOST
from components.layout import create_layout
from components.callbacks import register_callbacks

# Initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

# Configure layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT, host=HOST)