from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize
import os

owncloud_oauth_authorize = os.getenv(
    "OWNCLOUD_OAUTH_AUTHORIZE_URL", "https://sandbox.owncloud.org/oauth/authorize")
owncloud_oauth_token_url = os.getenv(
    "OWNCLOUD_OAUTH_ACCESS_TOKEN_URL", "https://sandbox.owncloud.org/oauth/token")
owncloud_oauth_id = os.getenv("OWNCLOUD_OAUTH_CLIENT_ID", "XY")
owncloud_oauth_secret = os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET", "ABC")


@FlaskOptimize.set_cache_timeout()
def index():
    return jsonify({
        "authorize_url": owncloud_oauth_authorize,
        "access_token_url": owncloud_oauth_token_url,
        "client_id": owncloud_oauth_id,
        "client_secret": owncloud_oauth_secret
    })
