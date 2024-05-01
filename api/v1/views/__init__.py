#!/usr/bin/python3
"""
Initialize the views module
"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')