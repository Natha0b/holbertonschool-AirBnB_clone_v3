#!/usr/bin/python3
"""
City objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities]), 200


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Returns the new City with the status code 201"""
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in city_json:
        return jsonify({'error': 'Missing name'}), 400
    city_json['state_id'] = state_id
    city = City(**city_json)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Returns the City object with the status code 200"""
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, val in city_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Returns an empty dictionary with the status code 200"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


if __name__ == '__main__':
    app_views.run(debug=True)
