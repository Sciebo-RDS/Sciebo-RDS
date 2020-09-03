#!/usr/bin/env python

from __init__ import app, register_service
import os


redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
osf_address = os.getenv("OPENSCIENCEFRAMEWORK_ADDRESS", "https://test.osf.io/")
osf_oauth_token_url = "{}/oauth/token".format(osf_address)
osf_oauth_id = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_ID", "XY")
osf_oauth_secret = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_SECRET", "ABC")

osf_oauth_authorize = "{}/oauth/authorize%3Fredirect_uri={}&response_type=code&scope%3Ddeposit%3Awrite%20deposit%3Aactions&client_id={}".format(
    osf_address, redirect_uri, osf_oauth_id
)

register_service(
    "OpenScienceFramework",
    osf_oauth_authorize,
    osf_oauth_token_url,
    osf_oauth_id,
    osf_oauth_secret
)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server='gevent')


