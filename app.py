#!/usr/bin/python3

from datetime import datetime
from flask import Flask
from pathlib import Path

# Import blueprints
from api.user_api import user_api
from api.country_api import country_api
from api.city_api import city_api
from api.amenity_api import amenity_api
from api.place_api import place_api
from api.review_api import review_api

# Initialize Flask app
app = Flask(__name__)

# Register blueprints - updated to unique prefixes
app.register_blueprint(user_api, url_prefix='/api/v1')
app.register_blueprint(country_api, url_prefix='/api/v1')
app.register_blueprint(city_api, url_prefix='/api/v1')
app.register_blueprint(amenity_api, url_prefix='/api/v1')
app.register_blueprint(place_api, url_prefix='/api/v1')
app.register_blueprint(review_api, url_prefix='/api/v1')

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
