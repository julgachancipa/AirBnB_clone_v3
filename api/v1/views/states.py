#!/usr/bin/python3
"""States api"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/states', strict_slashes=False)
def all_states():
    """return all states"""
    states_dict = storage.all('State')
    states_list = list(states_dict.values())
    json_list = []
    for s in states_list:
        json_list.append(s.to_dict())
    return jsonify(json_list)
