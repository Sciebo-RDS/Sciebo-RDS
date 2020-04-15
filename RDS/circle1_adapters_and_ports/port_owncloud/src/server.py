#!/usr/bin/env python

from __init__ import app, register_service
import os

register_service(
    "Owncloud",
    os.getenv("OWNCLOUD_OAUTH_AUTHORIZE_URL", "http://localhost:3000"),
    os.getenv("OWNCLOUD_OAUTH_ACCESS_TOKEN_URL", "http://localhost:3000"),
    os.getenv("OWNCLOUD_OAUTH_CLIEND_ID", ""),
    os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET", "")
)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server='gevent')
