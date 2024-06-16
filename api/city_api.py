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
from data import FileStorage
from data import (
    country_data, place_data, amenity_data,
    place_to_amenity_data, review_data, user_data, city_data
)

# Import utility functions
from utils import pretty_json

# Creates a blueprint 
city_api = Blueprint('city api', __name__)

# GET - Retrieve all cities.
@city_api.route('/cities', methods=["GET"])
def get_cities():
    """return all cities """
    cities_info = []

    for city_value in city_data.values():
        cities_info.append({
            "id": city_value["id"],
            "country_id": city_value["country_id"],
            "name": city_value["name"],
            "created_at": datetime.fromtimestamp(city_value["created_at"]).isoformat(),
            "updated_at": datetime.fromtimestamp(city_value["updated_at"]).isoformat()
        })

    return pretty_json(cities_info)

# GET - Retrieve details of a specific city by its ID.
@city_api.route('/cities/<city_id>', methods=["GET"])
def get_specific_city(city_id):
    """get specific city"""

    for city_value in city_data.values():
        if city_value["id"] == city_id:
            data = city_value
            break
    else:
        abort(404, f"User: {city_id} not found")

    city_info = {
        "id": data["id"],
        "country_id": data["country_id"],
        "name": data["name"],
        "created_at": datetime.fromtimestamp(data["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(data["updated_at"]).isoformat()
    }

    return pretty_json(city_info), 200

# POST - Create a new city.
@city_api.route('/cities', methods=["POST"])
def create_new_city():
    """create a new city to a specific country"""

    if not request.json:
        abort(400, "Request must contain JSON data")

    data = request.get_json()

    required_fields = ["name", "country_id"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        new_city = City(
            name=data["name"],
            country_id=data["country_id"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    city_data[new_city.id] = {
        "id": new_city.id,
        "country_id": new_city.country_id,
        "name": new_city.name,
        "created_at": new_city.created_at,
        "updated_at": new_city.updated_at
    }

    try:
        FileStorage.save_model_data("city_data.json", city_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": new_city.id,
        "country_id": new_city.country_id,
        "name": new_city.name,
        "created_at": datetime.fromtimestamp(new_city.created_at).isoformat(),
        "updated_at": datetime.fromtimestamp(new_city.updated_at).isoformat()
    }

    return pretty_json(attribs), 200

# PUT - Update data of a specific city.
@city_api.route('/cities/<city_id>', methods=["PUT"])
def update_city_data(city_id):
    """update data of a specific city"""
    if not request.json:
        abort(400, "Request must contain JSON data")

    new_data = request.get_json()

    for city_value in city_data.values():
        if city_value["id"] == city_id:
            found_city_data = city_value
            break
    else:
        abort(404, "City ID not found: {city_id}")

    if "name" in new_data:
        found_city_data["name"] = new_data["name"]

    try:
        FileStorage.save_model_data("city_data.json", city_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": found_city_data["id"],
        "country+id": found_city_data["country_id"],
        "name": found_city_data["name"],
        "created_at": datetime.fromtimestamp(found_city_data["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(found_city_data["updated_at"]).isoformat()
    }

    return pretty_json(attribs), 200

# DELETE - Delete a specific city.
@ city_api.route('/cities/<city_id>', methods=["DELETE"])
def delete_a_city(city_id):
    """delete a specific city"""

    keys_to_delete = []

    for city_key, city_value in list(city_data.items()):
        if city_value["id"] == city_id:
            keys_to_delete.append(city_key)

    if not keys_to_delete:
        abort(404, f"Place not found with ID: {city_id}")

    # Remove the place(s) from the dictionary
    for city_key in keys_to_delete:
        del city_data[city_key]

    try:
        FileStorage.save_model_data("city_data.json", city_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")
    # Return a confirmation message
    return pretty_json({"message": f"Place {city_id} has been deleted."}), 204
