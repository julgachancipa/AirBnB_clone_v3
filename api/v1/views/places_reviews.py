#!/usr/bin/python3
"""
Amenities api
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def show_r_places(place_id):
    """
    creates a new place
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    review_obj = place.reviews
    review_list = []
    for r in review_obj:
        review_list.append(r.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def r_place_id(review_id):
    """
    find a review by id
    """
    review = storage.get('Review', review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_r_place(review_id):
    """
    delete review id
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_r_place(place_id):
    """
    creates a new r_place
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    nw_review = Review(user_id=request.json['user_id'],
                       text=request.json['text'],
                       place_id=place_id)
    storage.new(nw_review)
    storage.save()
    return jsonify(nw_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_r_places(review_id):
    """
    update_task
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key in data:
        if key not in ['id', 'created_at', 'updated_at',
                       'user_id', 'place_id']:
            setattr(review, key, data[key])
    storage.save()
    return jsonify(review.to_dict()), 200
