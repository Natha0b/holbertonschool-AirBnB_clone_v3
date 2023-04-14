#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews]), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review_by_id(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Returns the new Review with the status code 201"""
    review_json = request.get_json(silent=True)
    if not review_json:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if 'user_id' not in review_json:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, review_json.get('user_id'))
    if not user:
        abort(404)
    if 'text' not in review_json:
        return jsonify({'error': 'Missing text'}), 400
    review_json['place_id'] = place_id
    review = Review(**review_json)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Returns the Review object with the status code 200"""
    review_json = request.get_json(silent=True)
    if not review_json:
        return jsonify({'error': 'Not a JSON'}), 400
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    for key, val in review_json.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
