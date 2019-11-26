from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize
import os

zenodo_oauth_authorize = os.getenv(
    "ZENODO_OAUTH_AUTHORIZE_URL", "https://sandbox.zenodo.org/oauth/authorize")
zenodo_oauth_token_url = os.getenv(
    "ZENODO_OAUTH_ACCESS_TOKEN_URL", "https://sandbox.zenodo.org/oauth/token")
zenodo_oauth_id = os.getenv("ZENODO_OAUTH_CLIEND_ID", "XY")
zenodo_oauth_secret = os.getenv("ZENODO_OAUTH_CLIENT_SECRET", "ABC")


@FlaskOptimize.set_cache_timeout()
def index():
    return jsonify({
        "authorize_url": zenodo_oauth_authorize,
        "access_token_url": zenodo_oauth_token_url,
        "client_id": zenodo_oauth_id,
        "client_secret": zenodo_oauth_secret
    })
