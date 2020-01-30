#!/usr/bin/python3
"""
Status of your API
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(error):
    """
    oh my cat
    """
    return (jsonify(error="Not found"), 404)


@app.teardown_appcontext
def close_s(x=None):
    """
    close session at the end
    """
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
