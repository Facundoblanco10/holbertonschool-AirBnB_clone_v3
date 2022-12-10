#!/usr/bin/python3
"""States"""

from flask import make_response, jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.state import State


@app_views.route("/states")
def state_index():
    states = storage.all(State).values()
    states_list = list(map(lambda state: state.to_dict(), states))
    return (json.dumps(states_list))


@app_views.route("/states/<state_id>")
def state_get(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return json.dumps(state.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def state_delete(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            state.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route("/states", methods=['POST'])
def state_post():
    try:
        data = request.get_json()
        if 'name' not in data:
            return make_response(jsonify({'message': 'Missing name'}), 400)
        state = State()
        state.name = data['name']
        storage.new(state)
        storage.save()
        return make_response(state.to_dict(), 201)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)


@app_views.route("/states/<state_id>", methods=['PUT'])
def state_update(state_id):
    try:
        data = request.get_json()
        states = storage.all(State).values()
        for state in states:
            if state.id == state_id:
                if "name" in data:
                    state.name = request.get_json()['name']
                storage.save()
                return make_response(state.to_dict(), 200)
        return make_response(jsonify({'error': 'Not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Not a JSON'}), 400)
