#!/usr/bin/env python

from __init__ import app, register_service
import os


redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
osf_address = os.getenv("OPENSCIENCEFRAMEWORK_ADDRESS", "https://accounts.test.osf.io")
osf_oauth_token_url = "{}/oauth2/token".format(osf_address)
osf_oauth_id = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_ID", "XY")
osf_oauth_secret = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_SECRET", "ABC")

osf_oauth_authorize = "{}/oauth2/authorize?response_type=code&redirect_uri={}&client_id={}&scope=osf.full_write&access_type={}".format(
    osf_address, redirect_uri, osf_oauth_id, "offline"
)

register_service(
    "Openscienceframework",
    osf_oauth_authorize,
    osf_oauth_token_url,
    osf_oauth_id,
    osf_oauth_secret,
)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server="gevent")

