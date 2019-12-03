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


def bootstrap(name='MicroService', executes=True):
    list_openapi = Util.load_oai(
        os.getenv("OPENAPI_FILEPATH", "central-service_token-storage.yml"))

    if not executes:
        app = App(name, use_default_error=True)
    else:
        app = App(name, all=True)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"))

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app

    ServerUtil.storage = Storage()
    if executes:
        app.run(port=8080, server='gevent')

    # return app for test or error handling purpose
    return app


if __name__ == "__main__":
    bootstrap("CentralServiceTokenStorage")
