#!/usr/bin/python3
"""
Create a new view for User object
that handles all default RESTFul API actions
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user_by_id(user_id):
    """Retrieves a User object id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """create user"""
    user_json = request.get_json(silent=True)
    if not user_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in user_json:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in user_json:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    user_json = request.get_json(silent=True)
    if not user_json:
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, val in user_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_users(user_id):
    """delete an user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
