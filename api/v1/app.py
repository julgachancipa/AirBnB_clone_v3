#!/usr/bin/python3
"""
Status of your API
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(error):
    """
    oh my cat
    """
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def close_s(x=None):
    """
    close session at the end
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
