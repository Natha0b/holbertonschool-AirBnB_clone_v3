#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places]), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Returns the new Place with the status code 201"""
    place_json = request.get_json(silent=True)
    if not place_json:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'user_id' not in place_json:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, place_json.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in place_json:
        return jsonify({'error': 'Missing name'}), 400
    place_json['city_id'] = city_id
    place = Place(**place_json)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Returns the Place object with the status code 200"""
    place_json = request.get_json(silent=True)
    if not place_json:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for key, val in place_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
