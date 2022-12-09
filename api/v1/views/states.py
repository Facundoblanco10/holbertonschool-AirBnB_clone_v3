#!/usr/bin/python3
"""States"""

from flask import make_response, jsonify
from api.v1.views import app_views
import json
from models import storage
from models.state import State


@app_views.route("/states")
def index():
    states = storage.all(State).values()
    states_list = list(map(lambda state: state.to_dict(), states))
    return (json.dumps(states_list))


@app_views.route("/states/<state_id>")
def get(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return json.dumps(state.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)
