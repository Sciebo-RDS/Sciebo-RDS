from connexion_plus import App, MultipleResourceResolver, Util

import json
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
import requests
from werkzeug.exceptions import abort

import logging, os

log_level = os.environ.get("LOGLEVEL", "DEBUG")
logger = logging.getLogger("")
logging.getLogger("").handlers = []
logging.basicConfig(format="%(asctime)s %(message)s", level=log_level)


def bootstrap(name="MicroService", *args, **kwargs):
    list_openapi = Util.load_oai(
        os.getenv(
            "OPENAPI_MULTIPLE_FILES",
            "../../circle2_use_cases/interface_port_metadata.yml"
        )
    )

    zenodo_address = None
    if "address" in kwargs:
        zenodo_address = kwargs["address"]
        del kwargs["address"]

    app = App(name, *args, **kwargs)

    app.app.zenodo_address = zenodo_address

    for oai in list_openapi:
        app.add_api(
            oai,
            resolver=MultipleResourceResolver("api", collection_endpoint_name="index"),
            validate_responses=True,
        )

    return app


app = bootstrap("PortZenodo", all=True)
