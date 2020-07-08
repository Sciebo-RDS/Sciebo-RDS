from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize
import os

owncloud_installation_url = os.getenv("OWNCLOUD_INSTALLATION_URL", "")
redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
owncloud_oauth_token_url = "{}/index.php/apps/oauth2/api/v1/token".format(
    owncloud_installation_url
)
owncloud_oauth_id = os.getenv("OWNCLOUD_OAUTH_CLIENT_ID", "XY")
owncloud_oauth_secret = os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET", "ABC")

owncloud_oauth_authorize = "{}/index.php/apps/oauth2/authorize?redirect_uri={}&response_type=code&client_id={}".format(
    owncloud_installation_url, redirect_uri, owncloud_oauth_id
)


@FlaskOptimize.set_cache_timeout()
def index():
    return jsonify(
        {
            "authorize_url": owncloud_oauth_authorize,
            "access_token_url": owncloud_oauth_token_url,
            "client_id": owncloud_oauth_id,
            "client_secret": owncloud_oauth_secret,
        }
    )
