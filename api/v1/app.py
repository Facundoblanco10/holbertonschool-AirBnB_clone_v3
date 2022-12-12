#!/usr/bin/python3
"""app"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exit):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", default="0.0.0.0")
    api_port = getenv("HBNB_API_PORT", default="5000")
    app.run(host=api_host, port=api_port, threaded=True)
