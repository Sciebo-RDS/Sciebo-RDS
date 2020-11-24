from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize
import os

redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
osf_address = os.getenv("OPENSCIENCEFRAMEWORK_ADDRESS", "https://accounts.test.osf.io")
osf_oauth_token_url = "{}/oauth2/token".format(osf_address)
osf_oauth_id = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_ID", "XY")
osf_oauth_secret = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_SECRET", "ABC")

osf_oauth_authorize = "{}/oauth2/authorize?response_type=code&redirect_uri={}&client_id={}&scope=osf.full_write".format(
    osf_address, redirect_uri, osf_oauth_id
)


@FlaskOptimize.set_cache_timeout()
def index():
    return jsonify(
        {
            "authorize_url": osf_oauth_authorize,
            "access_token_url": osf_oauth_token_url,
            "client_id": osf_oauth_id,
            "client_secret": osf_oauth_secret,
        }
    )
