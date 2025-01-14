#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def status():
    status = {
        "status": "OK"
        }
    return(status)


@app_views.route("/stats")
def stats():
    stats = {}
    for k, v in classes.items():
        stats[k] = storage.count(v)
    return stats
