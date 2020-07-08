from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize
import os

redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
zenodo_address = os.getenv("ZENODO_ADDRESS", "https://sandbox.zenodo.org")
zenodo_oauth_token_url = "{}/oauth/token".format(zenodo_address)
zenodo_oauth_id = os.getenv("ZENODO_OAUTH_CLIENT_ID", "XY")
zenodo_oauth_secret = os.getenv("ZENODO_OAUTH_CLIENT_SECRET", "ABC")

zenodo_oauth_authorize = "{}/oauth/authorize%3Fredirect_uri={}&response_type=code&scope=deposit%3Awrite+deposit%3Aactions&client_id={}".format(
    zenodo_address, redirect_uri, zenodo_oauth_id
)


@FlaskOptimize.set_cache_timeout()
def index():
    return jsonify(
        {
            "authorize_url": zenodo_oauth_authorize,
            "access_token_url": zenodo_oauth_token_url,
            "client_id": zenodo_oauth_id,
            "client_secret": zenodo_oauth_secret,
        }
    )
