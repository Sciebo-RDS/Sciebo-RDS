#!/usr/bin/env python

from __init__ import app, register_service
import os

owncloud_installation_url = os.getenv("OWNCLOUD_INSTALLATION_URL", "")
owncloud_redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
owncloud_oauth_token_url = "{}/index.php/apps/oauth2/api/v1/token".format(
    owncloud_installation_url
)
owncloud_oauth_id = os.getenv("OWNCLOUD_OAUTH_CLIENT_ID", "XY")
owncloud_oauth_secret = os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET", "ABC")

owncloud_oauth_authorize = "{}/index.php/apps/oauth2/authorize?redirect_uri={}&response_type=code&client_id={}".format(
    owncloud_installation_url, owncloud_redirect_uri, owncloud_oauth_id
)

register_service(
    "Owncloud",
    owncloud_oauth_authorize,
    owncloud_oauth_token_url,
    owncloud_oauth_id,
    owncloud_oauth_secret,
)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server="gevent")
