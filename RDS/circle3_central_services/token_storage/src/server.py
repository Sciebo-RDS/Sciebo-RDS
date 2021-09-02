#!/usr/bin/env python

from __init__ import bootstrap, ServerUtil

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app = bootstrap("CentralServiceTokenStorage", all=True)


@app.tracing.trace()
def fn():
    with app.tracing.tracer.start_active_span("Refresh tokens for services") as scope:
        scope.span.log_kv({'event': 'starts refreshing'})
        ServerUtil.storage.refresh_services()
        scope.span.log_kv({'event': 'finished refreshing'})


def refresh():
    with app.app.test_request_context('/refresh'):
        fn()


# add refresh func for refresh_tokens to scheduler and starts (https://stackoverflow.com/a/52068807)
app.scheduler.add_job(
    "refresh_service",
    refresh,
    trigger="interval",
    minutes=20,
)

app.run(port=8080, server="gevent")
