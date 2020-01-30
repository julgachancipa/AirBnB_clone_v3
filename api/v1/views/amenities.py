#!/usr/bin/python3
"""
Amenities api
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """
    return all amenities
    """
    amenities_dict = storage.all('Amenity')
    amenities_list = list(amenities_dict.values())
    json_list = []
    for a in amenities_list:
        json_list.append(a.to_dict())
    return jsonify(json_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenity_id(amenity_id):
    """
    find a city by id
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """
    delete amenity id
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    creates a new amenity
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not 'name' in request.get_json():
        abort(400, 'Missing name')
    nw_amenity = Amenity(name=request.json['name'])
    storage.new(nw_amenity)
    storage.save()
    return jsonify(nw_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    update_task
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key in data:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, data[key])
    storage.save()
    return jsonify(amenity.to_dict()), 200
