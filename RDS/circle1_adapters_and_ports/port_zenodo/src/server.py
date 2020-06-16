#!/usr/bin/env python

from __init__ import app, register_service
import os


register_service(
    "Zenodo",
    os.getenv("ZENODO_OAUTH_AUTHORIZE_URL"),
    os.getenv("ZENODO_OAUTH_ACCESS_TOKEN_URL"),
    os.getenv("ZENODO_OAUTH_CLIENT_ID"),
    os.getenv("ZENODO_OAUTH_CLIENT_SECRET")
)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server='gevent')


