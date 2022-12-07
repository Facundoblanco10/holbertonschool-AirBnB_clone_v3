#!/usr/bin/python3
"""init"""

from flask import Blueprint

app_views = Blueprint('v1', __name__,
                      url_prefix="/api/v1")
from api.v1.views.index import *
