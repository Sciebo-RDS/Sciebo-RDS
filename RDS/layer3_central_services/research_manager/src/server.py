#!/usr/bin/env python

import Singleton
from __init__ import bootstrap

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app = bootstrap("CentralServiceResearch", all=True)


@app.tracing.trace()
def fn_deprovizionize():
    with app.tracing.tracer.start_active_span("Deprovizionize users") as scope:
        scope.span.log_kv({"event": "starts deprovizionize"})
        Singleton.ProjectService.deprovizionize()
        scope.span.log_kv({"event": "finished deprovizionize"})


def deprovizionize():
    with app.app.test_request_context("/deprovizionize"):
        fn_deprovizionize()


app.scheduler.add_job(
    "deprov_projects",
    deprovizionize,
    trigger="interval",
    minutes=120,
)

app.run(port=8080, server="gevent")
