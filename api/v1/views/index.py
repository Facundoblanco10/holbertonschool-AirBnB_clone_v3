#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from models import storage
from models.engine.file_storage import classes


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
