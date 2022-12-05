#!/usr/bin/python3
"""index"""

from api.v1.views import app_views

@app_views.route("/status")
def index():
    status = {
        "status": "OK"
        }
    return(status)