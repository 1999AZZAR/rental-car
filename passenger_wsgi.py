import sys
import os

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import the Flask app object from app.py
from app import app

# Define the WSGI application object
application = app
