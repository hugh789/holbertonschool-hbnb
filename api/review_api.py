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
review_api = Blueprint('review_api', __name__)



@review_api.route('/reviews', methods=["GET"])
def reviews_get():
    """return all reviews"""
    reviewer_data = {}

    for review_value in review_data.values():
        review_place_id = review_value["place_id"]
        place_name = place_data[review_place_id]["name"]
        commentor_id = review_value["commentor_user_id"]
        reviewer_first_name = user_data[commentor_id]["first_name"]
        reviewer_last_name = user_data[commentor_id]["last_name"]

        if place_name not in reviewer_data:
            reviewer_data[place_name] = []

        reviewer_data[place_name].append({
            "review": review_value["feedback"],
            "rating": f"{review_value['rating']} / 5",
            "reviewer": f"{reviewer_first_name} {reviewer_last_name}",
            "created_at": datetime.fromtimestamp(review_value['created_at']).isoformat(),
            "updated_at": datetime.fromtimestamp(review_value['updated_at']).isoformat()
        })

    if not review_data:
        abort(404, "No Reviews available")

    return pretty_json(reviewer_data), 200


@review_api.route('/places/<place_id>/reviews', methods=['GET'])
def reviews_specific_get(place_id):
    """returns specufued review of a place"""

    reviewer_data = {}

    # Iterate through review_data to find reviews matching place_id
    for review_value in review_data.values():
        if review_value["place_id"] == place_id:
            review_place_id = review_value["place_id"]
            place_name = place_data[review_place_id]["name"]
            commentor_id = review_value["commentor_user_id"]
            reviewer_first_name = user_data[commentor_id]["first_name"]
            reviewer_last_name = user_data[commentor_id]["last_name"]

            if place_name not in reviewer_data:
                reviewer_data[place_name] = []

            reviewer_data[place_name].append({
                "review": review_value["feedback"],
                "rating": f"{review_value['rating']} / 5",
                "reviewer": f"{reviewer_first_name} {reviewer_last_name}",
                "created_at": datetime.fromtimestamp(review_value['created_at']).isoformat(),
                "updated_at": datetime.fromtimestamp(review_value['updated_at']).isoformat()
            })

    if not reviewer_data:
        abort(404, f"No reviews found for place with ID: {place_id}")

    return pretty_json(reviewer_data), 200


@review_api.route('/users/<user_id>/reviews', methods=['GET'])
def get_specific_review_from_user(user_id):
    """returns specufued review from user id"""

    reviewer_data = {}

    for review_value in review_data.values():
        if review_value["commentor_user_id"] != user_id:
            continue

        try:
            place_id = review_value["place_id"]
            place_name = place_data[place_id]["name"]
            reviewer_first_name = user_data[user_id]["first_name"]
            reviewer_last_name = user_data[user_id]["last_name"]

        except KeyError:
            # Skip this review if any required data is missing
            continue

        if place_name not in reviewer_data:
            reviewer_data[place_name] = []

        reviewer_data[place_name].append({
            "review_id": review_value["id"],
            "place_id": place_id,
            "place_name": place_name,
            "review": review_value["feedback"],
            "rating": f"{review_value['rating']} / 5",
            "reviewer": f"{reviewer_first_name} {reviewer_last_name}",
            "created_at": datetime.fromtimestamp(review_value['created_at']).isoformat(),
            "updated_at": datetime.fromtimestamp(review_value['updated_at']).isoformat()
        })

    if not reviewer_data:
        abort(404, f"No reviews found for user with ID: {user_id}")

    return pretty_json(reviewer_data), 200


@ review_api.route('/reviews/<review_id>', methods=['GET'])
def get_specific_review(review_id):
    """returns specufued review from review id"""

    review_info = []

    for review_value in review_data.values():
        if review_value["id"] == review_id:
            data = review_value

    if data["id"] != review_id:
        abort(400, f"Review: {review_id} not found")

    review_infos = {
        "id": data["id"],
        "commentor_user_id": data["commentor_user_id"],
        "place_id": data["place_id"],
        "feedback": data["feedback"],
        "rating": data["rating"],
        "created_at": datetime.fromtimestamp(data['created_at']).isoformat(),
        "updated_at": datetime.fromtimestamp(data['updated_at']).isoformat()
    }
    review_info.append(review_infos)

    return pretty_json(review_info), 200


@ review_api.route('/places/<place_id>/reviews', methods=["POST"])
def create_new_review(place_id):
    """create a new review to a place"""

    if not request.json:
        abort(400, "Request body must be JSON")

    data = request.get_json()

    required_fields = ["commentor_user_id", "place_id", "feedback", "rating"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing required field: {field}")

    if data["place_id"] != place_id:
        abort(400, "Mismatched place_id in URL and data")

    try:
        new_review = Review(
            commentor_user_id=data["commentor_user_id"],
            place_id=data["place_id"],
            feedback=data["feedback"],
            rating=data["rating"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    review_data[new_review.id] = {
        "id": new_review.id,
        "commentor_user_id": new_review.commentor_user_id,
        "place_id": new_review.place_id,
        "feedback": new_review.feedback,
        "rating": new_review.rating,
        "created_at": new_review.created_at,
        "updated_at": new_review.updated_at
    }

    try:
        FileStorage.save_model_data("review_data.json", review_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": new_review.id,
        "commentor_user_id": new_review.commentor_user_id,
        "place_id": new_review.place_id,
        "feedback": new_review.feedback,
        "rating": new_review.rating,
        "created_at": datetime.fromtimestamp(new_review.created_at).isoformat(),
        "updated_at": datetime.fromtimestamp(new_review.updated_at).isoformat()
    }

    return pretty_json(attribs), 201


@ review_api.route('/reviews/<place_id>', methods=["PUT"])
def update_review(place_id):
    """update review from a sepcific place id"""

    if not request.json:
        abort(400, "Not a JSON")

    new_data = request.get_json()

    for review_value in review_data.values():
        if review_value["place_id"] == place_id:
            found_review_data = review_value
            break
    else:
        abort(404, f"Review for the place: {place_id} is not found")

    # only feedback and rating are allowed to be modified
    if "feedback" in new_data:
        found_review_data["feedback"] = new_data["feedback"]
    if "rating" in new_data:
        found_review_data["rating"] = new_data["rating"]

    try:
        FileStorage.save_model_data("review_data.json", review_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    attribs = {
        "id": found_review_data["id"],
        "commentor_user_id": found_review_data["commentor_user_id"],
        "place_id": found_review_data["place_id"],
        "feedback": found_review_data["feedback"],
        "rating": found_review_data["rating"],
        "created_at": datetime.fromtimestamp(found_review_data["created_at"]).isoformat(),
        "updated_at": datetime.fromtimestamp(found_review_data["updated_at"]).isoformat()
    }

    return pretty_json(attribs), 200


@ review_api.route('/reviews/<review_id>', methods=["DELETE"])
def delete_review(review_id):
    """delete a review of a place"""

    keys_to_delete = []

    for review_key, review_value in list(review_data.items()):
        if review_value["id"] == review_id:
            keys_to_delete.append(review_key)

    if not keys_to_delete:
        abort(404, f"Place not found with ID: {review_id}")

    # Remove the place(s) from the dictionary
    for review_key in keys_to_delete:
        del review_data[review_key]

    try:
        FileStorage.save_model_data("review_data.json", review_data)
    except Exception as e:
        abort(500, f"Failed to save data: {str(e)}")

    # Return a confirmation message
    return pretty_json({"message": f"Review {review_id} has been deleted."}), 204

