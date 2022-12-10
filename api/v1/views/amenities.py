#!/usr/bin/python3
"""Amenities"""

from flask import make_response, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities")
def amenity_index():
    amenities = storage.all(Amenity).values()
    amenities_list = list(map(lambda amenity: amenity.to_dict(), amenities))
    return (json.dumps(amenities_list))


@app_views.route("/amenities/<amenity_id>")
def amenity_get(amenity_id):
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            return json.dumps(amenity.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route("/amenity/<amenity_id>", methods=['DELETE'])
def amenity_delete(amenity_id):
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route("/amenity", methods=['POST'])
def amenity_post():
    try:
        data = request.get_json()
        if 'name' not in data:
            return make_response(jsonify({'message': 'Missing name'}), 400)
        amenity = Amenity()
        amenity.name = data['name']
        storage.new(amenity)
        storage.save()
        return make_response(amenity.to_dict(), 201)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)


@app_views.route("/amenity/<amenity_id>", methods=['PUT'])
def amenity_update(amenity_id):
    try:
        data = request.get_json()
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            if amenity.id == amenity_id:
                if "name" in data:
                    amenity.name = request.get_json()['name']
                storage.save()
                return make_response(amenity.to_dict(), 200)
        return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)