""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from lib.Storage import Storage
import utility as ServerUtil
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from jaeger_client import Config as jConfig
from connexion_plus import App, MultipleResourceResolver, Util
from RDS import Util as CommonUtil

import logging, os

log_level = os.environ.get("LOGLEVEL", "DEBUG")
logger = logging.getLogger("")
logging.getLogger("").handlers = []
logging.basicConfig(format="%(asctime)s %(message)s", level=log_level)

def bootstrap(name="MicroService", *args, **kwargs):
    list_openapi = Util.load_oai("central-service_token-storage.yml")

    app = App(name, *args, **kwargs)
    CommonUtil.monkeypatch(app=app.app)

    for oai in list_openapi:
        app.add_api(
            oai,
            resolver=MultipleResourceResolver("api", collection_endpoint_name="index"),
            validate_responses=True,
        )

    # init token storage
    ServerUtil.storage = Storage()

    return app
