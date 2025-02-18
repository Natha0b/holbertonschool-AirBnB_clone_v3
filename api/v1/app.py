#!/usr/bin/python3
"""
script that starts a Flask web application.
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
from flask import jsonify
import os
from flask_cors import CORS

"""create a variable app, instance of Flask"""
app = Flask(__name__)

"""register the blueprint app_views"""
app.register_blueprint(app_views)

"""HTTP access control (CORS)"""
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """Closes the connection to the database"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)

    app.run(host=host, port=port, threaded=True)
