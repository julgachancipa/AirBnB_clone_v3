#!/usr/bin/python3
"""Amenities api"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_place(state_id):
    """creates a new state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not 'name' in request.get_json():
        abort(400, 'Missing name')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    nw_city = City(name=request.json['name'], state_id=state_id)
    storage.new(nw_city)
    storage.save()
    return jsonify(nw_city.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def place_id(user_id):
    """find a user by id"""
    users = storage.get('User', user_id)
    if users is not None:
        return jsonify(users.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_place(user_id):
    """delete user id"""
    users = storage.get('User', user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_places():
    """creates a new users"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not 'name' in request.get_json():
        abort(400, 'Missing name')
    nw_user = User(name=request.json['name'])
    storage.new(nw_user)
    storage.save()
    return jsonify(nw_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_places(user_id):
    """update_task"""
    users = storage.get('User', user_id)
    if users is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key in data:
        if key not in ['id','created_at','updated_at']:
            setattr(users, key, data[key])
    storage.save()
    return jsonify(users.to_dict()), 200
