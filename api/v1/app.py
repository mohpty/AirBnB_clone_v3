#!/usr/bin/python3
"""
    Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable
app = Flask(__name__)
swagger = Swagger(app)

# defining global strict slashes
app.url_map.strict_slashes = False

# flask server environmental init
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin resource sharing
cors = CORS(app, resources={r'/*': {'origins': host}})

# app_views BluePrints
app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method closes current db session
    """
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global route to handle all error status codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    This updates HTTPException class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
        main flask app
    """
    setup_global_errors()
    app.run(host=host, port=port)
