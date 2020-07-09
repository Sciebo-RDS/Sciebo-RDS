#!/usr/bin/env python

from __init__ import app
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server='gevent')