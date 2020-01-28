#!/usr/bin/python3
"""Status of your API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_s(x=None):
    """close session at the end"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """oh my cat"""
    error = jsonify({"error": "Not found"})
    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
