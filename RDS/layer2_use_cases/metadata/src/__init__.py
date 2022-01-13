import os
import logging
from RDS import Util as RDSUtil
from json import JSONEncoder, JSONDecoder
from connexion_plus import App, MultipleResourceResolver, Util
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from gevent import monkey

monkey.patch_all()


log_level = os.environ.get("LOGLEVEL", "DEBUG")
logger = logging.getLogger("")
logging.getLogger("").handlers = []
logging.basicConfig(format="%(asctime)s %(message)s", level=log_level)


def bootstrap(name="MicroService", *args, **kwargs):
    list_openapi = Util.load_oai("use-case_metadata.yml")

    app = App(name, *args, **kwargs)
    RDSUtil.monkeypatch(app=app)

    for oai in list_openapi:
        app.add_api(
            oai,
            resolver=MultipleResourceResolver(
                "api", collection_endpoint_name="index"),
            validate_responses=True,
        )

    return app


app = bootstrap("UseCaseMetadata", all=True)
