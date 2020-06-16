#!/usr/bin/env python

from __init__ import bootstrap

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app = bootstrap("CentralServiceResearch", all=True)
app.run(port=8080, server='gevent')