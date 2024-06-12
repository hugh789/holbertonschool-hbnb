#!/usr/bin/python3

from datetime import datetime
from flask import Flask

# Import models
from models.amenity import Amenity
from models.city import City
from models.country import Country
from models.place import Place
from models.review import Review
from models.user import User

# Import blueprints
from api.user_api import user_blueprint
from api.country_api import country_blueprint
from api.city_api import city_blueprint
from api.amenity_api import amenity_api
from api.place_api import place_blueprint
from api.review_api import review_blueprint

# Initialize Flask app
app = Flask(__name__)

# Register blueprints - updated to unique prefixes
app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(country_blueprint, url_prefix='/api/v1/countries')
app.register_blueprint(city_blueprint, url_prefix='/api/v1/cities')
app.register_blueprint(amenity_blueprint, url_prefix='/api/v1/amenities')
app.register_blueprint(place_blueprint, url_prefix='/api/v1/places')
app.register_blueprint(review_blueprint, url_prefix='/api/v1/reviews')

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
