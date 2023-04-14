#!/usr/bin/python3
"""
Create an endpoint that retrieves the
number of each objects by type:
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status',
                 strict_slashes=False, methods=['GET'])
def status():
    """Returns OK if endpoint was correctly created"""
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats',
                 strict_slashes=False, methods=['GET'])
def stats():
    """Returns number of each object by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage

    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    count = {}

    for key, val in classes.items():
        count[key] = storage.count(val)
    return jsonify(count), 200
