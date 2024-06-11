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


review_blueprint = Blueprint('review_api', __name__)


# @review_blueprint.route('/example/places_reviews')
# def example_places_reviews():
#     """ prints out reviews of places """
#     # return jsonify(review_data)

#     reviewer_data = {}

#     for review_value in review_data.values():
#         review_place_id = review_value["place_id"]
#         place_name = place_data[review_place_id]["name"]
#         commentor_id = review_value["commentor_user_id"]
#         reviewer_first_name = user_data[commentor_id]["first_name"]
#         reviewer_last_name = user_data[commentor_id]["last_name"]

#         if place_name not in reviewer_data:
#             reviewer_data[place_name] = []

#         reviewer_data[place_name].append({
#             "review": review_value["feedback"],
#             "rating": f"{review_value['rating']} / 5",
#             "reviewer": f"{reviewer_first_name} {reviewer_last_name}"
#         })

#     return jsonify(reviewer_data)


@review_blueprint.route('/reviews', methods=["GET"])
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
            "reviewer": f"{reviewer_first_name} {reviewer_last_name}"
        })

    if not review_data:
        abort(404, "No Reviews available")

    return jsonify(reviewer_data)


@review_blueprint.route('/reviews/<place_id>', methods=['GET'])
def reviews_specific_get(place_id):
    """returns specufued review of a place"""

    reviewer_data = {}

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
                "reviewer": f"{reviewer_first_name} {reviewer_last_name}"
            })

    if not review_data:
        abort(404, f"Review for {place_id} is not found")

    return jsonify(reviewer_data)


@review_blueprint.route('/reviews', methods=["POST"])
def create_new_review():
    """create a new review"""

    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()

    required_fields = ["commentor_user_id", "place_id", "feedback", "rating"]
    for field in required_fields:
        if field not in data:
            abort(400, f"Missing data: {field}")

    try:
        new_review = Review(
            commentor_user_id=data["commentor_user_id"],
            place_id=data["place_id"],
            feedback=data["feedback"],
            rating=data["rating"]
        )
    except ValueError as exc:
        abort(400, repr(exc))

    review_data.setdefault("Review", [])
    review_data["Review"].append({
        "id": new_review.id,
        "commentor_user_id": new_review.commentor_user_id,
        "place_id": new_review.place_id,
        "feedback": new_review.feedback,
        "rating": new_review.rating,
        "created_at": new_review.created_at,
        "updated_at": new_review.updated_at
    })

    attribs = {
        "id": new_review.id,
        "commentor_user_id": new_review.commentor_user_id,
        "place_id": new_review.place_id,
        "feedback": new_review.feedback,
        "rating": new_review.rating,
        "created_at": datetime.fromtimestamp(new_review.created_at),
        "updated_at": datetime.fromtimestamp(new_review.updated_at)
    }

    return jsonify(attribs), 201


@review_blueprint.route('/reviews/<place_id>', methods=["PUT"])
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

    attribs = {
        "id": found_review_data["id"],
        "commentor_user_id": found_review_data["commentor_user_id"],
        "place_id": found_review_data["place_id"],
        "feedback": found_review_data["feedback"],
        "rating": found_review_data["rating"],
        "created_at": datetime.fromtimestamp(found_review_data["created_at"]),
        "updated_at": datetime.fromtimestamp(found_review_data["updated_at"])
    }

    return jsonify(attribs), 201


@review_blueprint.route('/reviews/<place_id>', methods=["DELETE"])
def delete_review(place_id):
    """delete a review of a place"""

    for review_value in review_data.values():
        if review_value["place_id"] == place_id:
            delete_review_data = review_value
            break
    else:
        abort(404, f"Review for the place: {place_id} is not found")

    review_info = {
        "id": delete_review_data["id"],
        "commentor_user_id": delete_review_data["commentor_user_id"],
        "place_id": delete_review_data["place_id"],
        "feedback": delete_review_data["feedback"],
        "rating": delete_review_data["rating"],
        "created_at": datetime.fromtimestamp(delete_review_data["created_at"]),
        "updated_at": datetime.fromtimestamp(delete_review_data["updated_at"])
    }

    return jsonify(review_info), 201