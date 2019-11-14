from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize


@FlaskOptimize.set_cache_timeout()
def search():
    return jsonify({"authorize_url": "https://example.org/authorize/",
                    "access_token_url": "https://example.org/oauth2/token",
                    "client_id": "xy_ab",
                    "client_secret": "ABC"})
