#!/usr/bin/env python

from __init__ import bootstrap, ServerUtil

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app = bootstrap("CentralServiceTokenStorage", all=True)

# add refresh func for refresh_tokens to scheduler and starts (https://stackoverflow.com/a/52068807)
app.scheduler.add_job("refresh_service",
                      ServerUtil.storage.refresh_services, trigger='interval', minutes=20)

app.run(port=8080, server='gevent')
