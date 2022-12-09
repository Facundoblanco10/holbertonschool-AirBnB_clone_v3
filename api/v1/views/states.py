#!/usr/bin/python3
"""States"""

from api.v1.views import app_views
import json
from models import storage
from models.state import State


@app_views.route("/states")
def index():
    states = storage.all(State).values()
    states_list = list(map(lambda state: state.to_dict(), states))
    return (json.dumps(states_list))