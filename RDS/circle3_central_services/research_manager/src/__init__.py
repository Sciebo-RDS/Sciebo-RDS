""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from jaeger_client import Config as jConfig

from connexion_plus import App, MultipleResourceResolver, Util
import Singleton
from lib.ProjectService import ProjectService
from RDS import Util as RDSUtil

import logging, os

log_level = os.environ.get("LOGLEVEL", "DEBUG")
logger = logging.getLogger("")
logging.getLogger("").handlers = []
logging.basicConfig(format="%(asctime)s %(message)s", level=log_level)


def bootstrap(name="MicroService", *args, **kwargs):
    list_openapi = Util.load_oai("central-service_research-manager.yml")

    app = App(name, *args, **kwargs)
    RDSUtil.monkeypatch("getDict", app=app.app)

    Singleton.ProjectService = ProjectService()

    for oai in list_openapi:
        app.add_api(
            oai,
            resolver=MultipleResourceResolver("api", collection_endpoint_name="index"),
            validate_responses=True,
        )

    return app
