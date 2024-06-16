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

# Create a blueprint
place_api = Blueprint('place_api', __name__)


@place_api.route('/example/places_amenties_raw')
def example_places_amenities_raw():
    """ Prints out the raw data for relationships between places and their amenities """
    return jsonify(place_to_amenity_data)


@place_api.route('/places_amenties', methods=["GET"])
def places_amenties():
    """ Prints out the relationships between places and their amenities using names """

    output = {}

    for place_key in place_to_amenity_data:
        place_name = place_data[place_key]['name']
        if place_name not in output:
            output[place_name] = []

        amenities_ids = place_to_amenity_data[place_key]
        for amenity_key in amenities_ids:
            amenity_name = amenity_data[amenity_key]['name']
            output[place_name].append(amenity_name)

    return pretty_json(output)


@place_api.route('/places', methods=["GET"])
def place_amenties():
    """get all places data"""

    places_info = []

    for place_value in place_data.values():
        places_info.append({
            "id": place_value["id"],
            "host_user_id": place_value["host_user_id"],
            "city_id": place_value["city_id"],
            "name": place_value["name"],
            "description": place_value["description"],
            "address": place_value["address"],
            "latitude": place_value["latitude"],
            "longitude": place_value["longitude"],
            "number_of_rooms": place_value["number_of_rooms"],
            "bathrooms": place_value["bathrooms"],
            "price_per_night": place_value["price_per_night"],
            "max_guests": place_value["max_guests"],
            "created_at": datetime.fromtimestamp(place_value["created_at"]).isoformat(),
            "updated_at": datetime.fromtimestamp(place_value["updated_at"]).isoformat()
        })

    return pretty_json(places_info), 200


@place_api.route('/places/<place_id>', methods=["GET"])
def place_info(place_id):
    """get sepecific info of a place"""
    for place_value in place_data.values():
        if place_value["id"] == place_id:
            found_place = place_value
            break
    else:
        abort(404, f"Place: {place_id} not found")

    place_info = {
        "id": found_place["id"],
        "host_user_id": found_place["host_user_id"],
        "city_id": found_place["city_id"],
        "name": found_place["name"],
        "description": found_place["description"],
        "address": found_place["address"],
        "latitude": found_place["latitude"],
        "longitude": found_place["longitude"],
        "number_of_rooms": found_place["number_of_rooms"],
        "bathrooms": found_place["bathrooms"],
        "price_per_night": found_place["price_per_night"],
        "max_guests": found_place["max_guests"],
        "created_at": datetime.fromtimestamp(found_place["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(found_place["updated_at"]).isoformat()
    }

    return pretty_json(place_info), 200


@place_api.route('/places', methods=["POST"])
def create_place_info():
    """create a new place"""
    if not request.json:
        abort(400, "Request must contain JSON data")

    data = request.get_json()

    required_fields = ["name", "description", "address", "latitude", "longitude",
                       "number_of_rooms", "bathrooms", "price_per_night", "max_guests"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        new_place = Place(
            host_user_id=data["host_user_id"],
            city_id=data["city_id"],
            name=data["name"],
            description=data["description"],
            address=data["address"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            number_of_rooms=data["number_of_rooms"],
            bathrooms=data["bathrooms"],
            price_per_night=data["price_per_night"],
            max_guests=data["max_guests"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    place_data[new_place.id] = {
        "id": new_place.id,
        "host_user_id": new_place.host_user_id,
        "city_id": new_place.city_id,
        "name": new_place.name,
        "description": new_place.description,
        "address": new_place.address,
        "latitude": new_place.latitude,
        "longitude": new_place.longitude,
        "number_of_rooms": new_place.number_of_rooms,
        "bathrooms": new_place.bathrooms,
        "price_per_night": new_place.price_per_night,
        "max_guests": new_place.max_guests,
        "created_at": new_place.created_at,
        "updated_at": new_place.updated_at
    }

    try:
        FileStorage.save_model_data("place_data.json", place_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": new_place.id,
        "host_user_id": new_place.host_user_id,
        "city_id": new_place.city_id,
        "name": new_place.name,
        "description": new_place.description,
        "address": new_place.address,
        "latitude": new_place.latitude,
        "longitude": new_place.longitude,
        "number_of_rooms": new_place.number_of_rooms,
        "bathrooms": new_place.bathrooms,
        "price_per_night": new_place.price_per_night,
        "max_guests": new_place.max_guests,
        "created_at": datetime.fromtimestamp(new_place.created_at).isoformat(),
        "updated_at": datetime.fromtimestamp(new_place.updated_at).isoformat()
    }

    return pretty_json(attribs), 200


@place_api.route('/places/<place_id>', methods=["PUT"])
def update_place_info(place_id):
    """update info of a place"""
    if not request.json:
        abort(400, "Not a JSON")

    new_data = request.get_json()

    for place_value in place_data.values():
        if place_value["id"] == place_id:
            found_place_data = place_value
            break
    else:
        abort(404, f"Place ID not found: {place_id}")

    # List of fields that can be updated
    updated_fields = ["name", "description", "address", "latitude", "longitude",
                      "number_of_rooms", "bathrooms", "price_per_night", "max_guests"]

    # use for loop for updateing fields
    for field in updated_fields:
        if field in new_data:
            found_place_data[field] = new_data[field]

    try:
        FileStorage.save_model_data("place_data.json", place_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": found_place_data["id"],
        "host_user_id": found_place_data["host_user_id"],
        "city_id": found_place_data["city_id"],
        "name": found_place_data["name"],
        "description": found_place_data["description"],
        "address": found_place_data["address"],
        "latitude": found_place_data["latitude"],
        "longitude": found_place_data["longitude"],
        "number_of_rooms": found_place_data["number_of_rooms"],
        "bathrooms": found_place_data["bathrooms"],
        "price_per_night": found_place_data["price_per_night"],
        "max_guests": found_place_data["max_guests"],
        "created_at": datetime.fromtimestamp(found_place_data["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(found_place_data["updated_at"]).isoformat()
    }

    return pretty_json(attribs), 200


@ place_api.route('/places/<place_id>', methods=["DELETE"])
def delete_place_info(place_id):
    """delete a place"""

    # Create a list of keys in place_data
    keys_to_delete = []

    for place_key, place_value in list(place_data.items()):
        if place_value["id"] == place_id:
            keys_to_delete.append(place_key)

    if not keys_to_delete:
        abort(404, f"Place not found with ID: {place_id}")

    # Remove the place(s) from the dictionary
    for place_key in keys_to_delete:
        del place_data[place_key]

    try:
        FileStorage.save_model_data("place_data.json", place_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    # Return a confirmation message
    return pretty_json({"message": f"Place {place_id} has been deleted."}), 204