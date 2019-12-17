from connexion_plus import App, MultipleResourceResolver, Util

import logging
import os
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

import Util as ServerUtil
from lib.Storage import Storage

log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def monkeypatch():
    """ Module that monkey-patches json module when it's imported so
    JSONEncoder.default() automatically checks for a special "to_json()"
    method and uses it to encode the object if found.
    """
    from json import JSONEncoder, JSONDecoder

    def to_default(self, obj):
        return getattr(obj.__class__, "to_json", to_default.default)(obj)

    to_default.default = JSONEncoder.default  # Save unmodified default.
    JSONEncoder.default = to_default  # Replace it.


def bootstrap(name='MicroService', *args, **kwargs):
    list_openapi = Util.load_oai(
        os.getenv("OPENAPI_FILEPATH", "central-service_token-storage.yml"))

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"), validate_responses=True)

    # init token storage
    ServerUtil.storage = Storage()

    return app


if __name__ == "__main__":
    monkeypatch()
    app = bootstrap("CentralServiceTokenStorage", all=True)

    # add refresh func for refresh_tokens to scheduler and starts (https://stackoverflow.com/a/52068807)
    app.scheduler.add_job("refresh_service",
                          ServerUtil.storage.refresh_services, trigger='interval', minutes=20)

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    app.run(port=8080, server='gevent')
