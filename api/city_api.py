#!/usr/bin/python3

from flask import Blueprint, jsonify, request, abort
from datetime import datetime

# Import models
from models.user import User
from models.review import Review
from models.place import Place
from models.country import Country
from models.city import City
from models.amenity import Amenity

# Import data
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)


city_blueprint = Blueprint('city api', __name__)


@city_blueprint.route('example/cities')
def example_cities():
    """ Example route to showing usage of the City model class"""

    # We will be appending dictionaries to the list instead of City objects
    # This is so we can print out on the webpage
    # If there is no need to display the data, we can consider storing the City objecects themselves
    cities_list = []

    # the 'hello' and 'world' params below will be filtered off in City constructor
    cities_list.append(City(name="Gotham", hello="hello").to_dict())
    cities_list.append(City(name="Metropolis", world="world").to_dict())

    # Validation: The city with a invalid name is not appended to the list
    try: 
        cities_list.append(City(name="#$%^&**", country_id=2).__dict__)
    except ValueError as exc:
        # This is printed internally in the server output. Not shown on website. 
        print("City creation Error - ", exc)

    # Validation: The city with a invalid country_id is not appended to the list
    try:
        cities_list.append(City(name="Duckburg", country_id=1234).__dict__)
    except ValueError as exc:
        print("City creation Error - ", exc)
    
    #Note that private attributes have a weird key format. e.g. "_City__country_id"
    # This shows that the output of the City object's built-in __dict__ is not usable as-is
    
    return cities_list

# GET /countries/{country_code}/cities: Retrieve all cities belonging to a specific country.
@city_blueprint.route('countries/<country_code>/cities', methods=['GET'])
def countries_cities(country_code):
    """ Return a list of cities in a country """
    data = []
    wanted_country_id = ""

    for k, v in country_data.items():
        if v['code'] == country_code:
            wanted_country_id = v['id']
    
    for k, v in city_data.items():
        if v['country_id'] == wanted_country_id:
            data.append({
                "id": v['id'],
                "name": v['name'],
                "country_id": v['country_id'],
                "created_at": datetime.fromtimestamp(v['created_at']),
                "updated_at": datetime.fromtimestamp(v['updated_at'])
            })

    return jsonify(data)