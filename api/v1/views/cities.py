#!/usr/bin/python3
"""Cities"""

from flask import make_response, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities')
def city_index(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return json.dumps(list(map(lambda city: city.to_dict(),
                              state.cities)))
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>')
def city_get(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            return json.dumps(city.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            city.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/states/<state_id>/cities', methods=["POST"])
def city_post(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            try:
                data = request.get_json()
                if 'name' not in data:
                    return make_response(jsonify({'message': 'Missing name'}), 400)
                city = City()
                city.name = data['name']
                city.state_id = state.id
                storage.new(city)
                storage.save()
                return make_response(city.to_dict(), 201)
            except Exception:
                return make_response(jsonify({'message': 'Not a JSON'}), 400)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
    try:
        data = request.get_json()
        cities = storage.all(City).values()
        for city in cities:
            if city.id == city_id:
                if "name" in data:
                    city.name = request.get_json()['name']
                storage.save()
                return make_response(city.to_dict(), 200)
        return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)
