#!/usr/bin/python3
"""Amenities api"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def all_users():
    """return all places"""
    users_dict = storage.all('State')
    users_list = list(users_dict.values())
    json_list = []
    for u in users_list:
        json_list.append(u.to_dict())
    return jsonify(json_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user_id(user_id):
    """find a user by id"""
    users = storage.get('User', user_id)
    if users is not None:
        return jsonify(users.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """delete user id"""
    users = storage.get('User', user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_users():
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
def update_users(user_id):
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
