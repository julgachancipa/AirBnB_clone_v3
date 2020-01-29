#!/usr/bin/python3
"""States api"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def state_cities(state_id):
    """find a state's cities"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    city_obj = state.cities
    city_list = []
    for c in city_obj:
        city_list.append(c.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_id(city_id):
    """find a city by id"""
    city = storage.get('City', city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """delete city id"""
    city = storage.get('City', city_id)
    if city is not None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
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


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update_task"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key in data:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, data[key])
    storage.save()
    return jsonify(city.to_dict()), 200
