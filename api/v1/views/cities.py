#!/usr/bin/python3
"""States api"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def state_cities(state_id):
    """find a state's cities"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    print('>>>', state)
    return jsonify({'oli': 'olis'})
