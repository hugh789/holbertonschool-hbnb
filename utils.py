from flask import jsonify


def pretty_json(data):
    """Utility function to return pretty-printed JSON response"""
    response = jsonify(data)
    response.headers.add('Content-Type', 'application/json')
    return response