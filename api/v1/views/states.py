#!/usr/bin/python3
"""States api"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """return all states"""
    states_dict = storage.all('State')
    states_list = list(states_dict.values())
    json_list = []
    for s in states_list:
        json_list.append(s.to_dict())
    return jsonify(json_list)


@app_views.route('/states/<state_id>')
def state_id(state_id):
    """find a state by id"""
    state = storage.get('State', state_id)
    if state != None:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """delete state id"""
    state = storage.get('State', state_id)
    if state == None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    if not request.json:
        abort(400, 'Not a JSON')
    if not 'name' in request.get_json():
        abort(400, 'Missing name')
    print(request.json)
    nw_state = State(name=request.json['name'])
    print('>>>', request.get_json())
    storage.new(nw_state)
    storage.save()
    return jsonify(nw_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state():
    """update_task"""
    state = storage.get('State', state_id)
    if state == None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items()
        if key not in ['id','created_at','updated_at']
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
