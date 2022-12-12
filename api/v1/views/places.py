#!/usr/bin/python3
"""Places"""

from flask import make_response, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.places import Places
from models.city import City


@app_views.route('/cities/<city_id>/places')
def place_index(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            return json.dumps(list(map(lambda place: place.to_dict(),
                              city.places)))
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/places/<place_id>')
def place_get(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            return json.dumps(place.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            place.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>/places', methods=["POST"])
def place_post(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            try:
                data = request.get_json()
                if 'name' not in data:
                    return make_response(jsonify({'message': 'Missing name'}),
                                         400)
                place = Place()
                place.name = data['name']
                place.description = data['description']
                place.number_rooms = data['number_rooms']
                place.number_bathrooms = data['number_bathrooms']
                place.max_guest = data['max_guest']
                place.price_by_night = data['price_by_night']
                place.latitude = data['latitude']
                place.longitude = data['longitude']
                place.city_id = city.id
                storage.new(place)
                storage.save()
                return make_response(place.to_dict(), 201)
            except Exception:
                return make_response(jsonify({'message': 'Not a JSON'}), 400)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id):
    try:
        data = request.get_json()
        places = storage.all(Place).values()
        for place in places:
            if place.id == place_id:
                if "name" in data:
                    place.name = request.get_json()['name']
                if "description" in data:
                    place.description = data['description']
                if "number_rooms" in data:
                    place.number_rooms = data['number_rooms']
                if "number_bathrooms" in data:
                    place.number_bathrooms = data['number_bathrooms']
                if "max_guest" in data:
                    place.max_guest = data['max_guest']
                if "price_by_night" in data:
                    place.price_by_night = data['price_by_night']
                if "latitude" in data:
                    place.latitude = data['latitude']
                if "longitude" in data:
                    place.longitude = data['longitude']
                storage.save()
                return make_response(place.to_dict(), 200)
        return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)
