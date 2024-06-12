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

country_api = Blueprint('country_api', __name__)


# Examples
@country_api.route('/example/country_data')
def example_country_data():
    """ Example to show that we can view data loaded in the data module's init """
    return jsonify(country_data)

#GET /countries: Retrieve all pre-loaded countries.
@country_api.route('/countries', methods=["GET"])
def countries_get():
    """ returns all countires data """

    countries_info = []
    for country_value in country_data.values():
        countries_info.append({
            "id": country_value["id"],
            "name": country_value["name"],
            "code": country_value["code"],
            "created_at": datetime.fromtimestamp(country_value["created_at"]),
            "updated_at": datetime.fromtimestamp(country_value["updated_at"])
        })

    return jsonify(countries_info)

#GET /countries/{country_code}: Retrieve details of a specific country by its code.
@country_api.route('/countries/<country_code>', methods=["GET"])
def countries_specific_get(country_code):
    """ returns specific country data """

    for country_value in country_data.values():
        if country_value['code'] == country_code:
            data = country_value

    country_info = {
        "id": data['id'],
        "name": data['name'],
        "code": data['code'],
        "created_at": datetime.fromtimestamp(data['created_at']),
        "updated_at": datetime.fromtimestamp(data['updated_at'])
    }

    return jsonify(country_info)


@country_api.route('/countries', methods=["POST"])
def create_new_country():
    """ posts data for new country then returns the country data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'
    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()
    country_list = data.get("Country")

    for data in country_list:
        # Check for required fields in each country data
        required_fields = ["name", "code"]
        for field in required_fields:
            if field not in data:
                abort(400, f"Missing required field: {field}")
        try:
            new_country = Country(
                name=data["name"],
                code=data["code"]
            )
        except ValueError as exc:
            abort(400, repr(exc))

        country_data.setdefault("Country", [])
        # country_data.setdefault("Country", [])
        country_data["Country"].append({
            "id": new_country.id,
            "name": new_country.name,
            "code": new_country.code,
            "created_at": new_country.created_at,
            "updated_at": new_country.updated_at
        })
        attribs = {
            "id": new_country.id,
            "name": new_country.name,
            "code": new_country.code,
            "created_at": datetime.fromtimestamp(new_country.created_at),
            "updated_at": datetime.fromtimestamp(new_country.updated_at)
        }
        return jsonify(attribs), 201
    

#@country_api.route('/countries/<country_code>', methods=["PUT"])
#def update_country(country_code):
        """" updates existing user data using specified id """
        abort(400, "Not a JSON")

    new_data = request.get_json()

    # Search for the country with the specified country_code
    #for country_value in country_data.values():
        #if country_value["code"] == country_code:
            #found_country_data = country_value
            #break
    #else:
        #abort(404, f"Country not found: {country_code}")

    # Update country attributes if new data is provided
    #if "name" in new_data:
        #found_country_data["name"] = new_data["name"]
   # if "code" in new_data:
        #found_country_data["code"] = new_data["code"]

    # Prepare response attributes with updated timestamps as datetime objects
   # attribs = {
        #"id": found_country_data["id"],
       # "name": found_country_data["name"],
       # "code": found_country_data["code"],
       # "created_at": datetime.fromtimestamp(found_country_data["created_at"]), 
       # "updated_at": datetime.fromtimestamp(found_country_data["updated_at"]) 
    

    #return jsonify(attribs), 200


@country_api.route('/countries/<country_code>', methods=["DELETE"])
def delete_country(country_code):
    """Deletes an existing user by user_id"""
    
    # Check if user_id exists in user_data
    for country_value in country_data.values():
        if country_value["code"] == country_code:
            delete_data = country_value
            break
    else:
        abort(404, f"Country not found: {country_code}")

    country_info = {
        "id": delete_data["id"],
        "code": delete_data["code"],
        "name": delete_data["name"],
        "created_at": datetime.fromtimestamp(delete_data["created_at"]),
        "updated_at": datetime.fromtimestamp(delete_data["updated_at"])
    }

    return jsonify(country_info), 200