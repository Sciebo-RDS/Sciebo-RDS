from connexion_plus import App, MultipleResourceResolver, Util

import logging
import os
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

import Util as ServerUtil
from lib.Storage import Storage
from flask import jsonify

log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def bootstrap(name='MicroService'):
    list_openapi = Util.load_oai(
        os.getenv("OPENAPI_FILEPATH", "central-service_token-storage.yml"))

    # for simpler testing usage
    app = App(name, use_default_error=True) if __name__ is not "__main__" else App(
        name, all=True)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"))

    # init token storage
    ServerUtil.storage = Storage()

    return app


if __name__ == "__main__":
    app = bootstrap("CentralServiceTokenStorage")

    # add refresh func for refresh_tokens to scheduler and starts (https://stackoverflow.com/a/52068807)
    app.scheduler.add_job(
        ServerUtil.storage.refresh_services, 'interval', minutes=20)
    app.scheduler.start()

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    app.run(port=8080, server='gevent')
