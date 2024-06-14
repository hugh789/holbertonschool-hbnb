#!/usr/bin/python3

from flask import Blueprint, jsonify, request, abort
from datetime import datetime
from pathlib import Path

# Import Models
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

# Define the blueprint for user_api
user_api = Blueprint('user api', __name__ )

#GET /users: Retrieve a list of all users.
@user_api.route('/users', methods=["GET"])
def users_get():
    """ Get/return all users """

    users_info = []
    for user_value in user_data.values():
        users_info.append({
            "id": user_value['id'],
            "first_name": user_value['first_name'],
            "last_name": user_value['last_name'],
            "email": user_value['email'],
            "password": user_value['password'],
            "created_at": datetime.fromtimestamp(user_value['created_at']),
            "updated_at": datetime.fromtimestamp(user_value['updated_at'])
        })

    return jsonify(users_info)

#GET /users/{user_id}: Retrieve details of a specific user.
@user_api.route('/users/<user_id>', methods=["GET"])
def users_specific_get(user_id):
    """ Get/return a specific user """

    for user_value in user_data.values():
        if user_value["id"] == user_id:
            data = user_value
            break
    else:
        abort(404, description="User not found")
    
    user_info = {
        "id": data['id'],
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email": data['email'],
        "password": data['password'],
        "created_at": datetime.fromtimestamp(data['created_at']),
        "updated_at": datetime.fromtimestamp(data['updated_at'])
    }

    return jsonify(user_info)

#POST /users: Create a new user.
@user_api.route('/users', methods=["POST"])
def create_new_user():
    """ Create a new user """
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    if not request.json:
        abort(400, description="Not a JSON")

    # convert to python dict data type
    data = request.get_json()
    user_list = data.get("User")

    for data in user_list:
        required_fields = ["first_name", "last_name", "email", "password"]
        for field in required_fields:
            if field not in data:
                abort(400, f"Misssing data: {field}")
        
        try:
            #use User class to create a new object and
            # access method: dict
            new_user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=data["password"]
            )
        except ValueError as exc:
            abort(400, repr(exc))

        # setdefault ("User", []) provides a safety net
        # by initializing "User" if absent
        user_data.setdefault("User", [])
        # add new user data to user_data
        # note that the created_at  and updated_at are usig timestamps
        # data stores -> serve side
        user_data["User"].append({
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "created_at": new_user.created_at.timestamp(),
            "updated_at": new_user.updated_at.timestamp()
        })

        # Prepare attributes to return, response to API request -> client side
        attribs = {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "created_at": datetime.fromtimestamp(new_user.created_at),
            "updated_at": datetime.fromtimestamp(new_user.updated_at)
        }
        FileStorage.save_model_data("new_user_test.json", new_user)
    
    return jsonify(attribs), 201

# PUT /users/{user_id}: Update an existing user.
@user_api.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # Check if request contains JSON data
    if not request.json:
        abort(400, description="Request must contain JSON data")
    
    # Get JSON data from request
    new_data = request.get_json()

    for user_value in user_data.values():
        if user_value["id"] == user_id:
            found_user_data = user_value
            break
    else:
        abort(404, f"User ID not found: {user_id}")
    
    # Update user's first_name and last_name if provided in JSON data
    if "first_name" in new_data:
        found_user_data["first_name"] = new_data["first_name"]
    if "last_name" in new_data:
        found_user_data["last_name"] = new_data["last_name"]
    
    # Update user_data with the modified found_user_data
    user_data[user_id] = found_user_data

    # Prepare response attributes with updated timestamps as datetime objects
    attribs = {
        "id": found_user_data["id"],
        "first_name": found_user_data["first_name"],
        "last_name": found_user_data["last_name"],
        "email": found_user_data["email"],
        "created_at": datetime.fromtimestamp(found_user_data["created_at"]),
        "updated_at": datetime.fromtimestamp(found_user_data["updated_at"])
    }
    #Call static method to persist changes (assuming user_data is a dictionary)
    FileStorage.save_model_data("testing.json", found_user_data)
     
    # Return JSON response with updated user attributes
    return jsonify(attribs), 200

#DELETE /users/{user_id}: Delete a user.
@user_api.route('/users/<user_id>', methods=["DELETE"])  
def delete_user(user_id):
    """ Delete a user using the specified id """
    
    # Check if user_id exists in user_data
    for user_value in user_data.values():
        if user_value["id"] == user_id:
            del user_data[user_id]
            break
    else:
        abort(404, f"User ID not found: {user_id}")

    user_info = {
        "id": delete_data['id'],
        "first_name": delete_data['first_name'],
        "last_name": delete_data['last_name'],
        "email": delete_data['email'],
        "password": delete_data['password'],
        "created_at": datetime.fromtimestamp(delete_data['created_at']),
        "updated_at": datetime.fromtimestamp(delete_data['updated_at'])
    }

    return jsonify(user_info), 200