#!/usr/bin/python3
"""Amenities api"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import places_reviews

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """creates a new place"""
    place = storage.get('Review', review_id)
    if place is None:
        abort(404)
    review_obj = place.reviews
    review_list = []
    for r in review_obj:
        review_list.append(r.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def place_id(user_id):
    """find a review by id"""
    review = storage.get('Place', place_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """delete review id"""
    review = storage.get('Place', place_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_place(place_id):
    """creates a new place"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not 'name' in request.get_json():
        abort(400, 'Missing name')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    nw_review = Review(name=request.json['name'], place_id=place_id)
    storage.new(nw_review)
    storage.save()
    return jsonify(nw_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_places(user_id):
    """update_task"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key in data:
        if key not in ['id','created_at','updated_at']:
            setattr(review, key, data[key])
    storage.save()
    return jsonify(review.to_dict()), 200
