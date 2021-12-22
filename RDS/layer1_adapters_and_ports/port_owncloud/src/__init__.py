from connexion_plus import App, MultipleResourceResolver, Util

import json
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
import requests

import logging
import os

log_level = os.environ.get("LOGLEVEL", "DEBUG")
logger = logging.getLogger("")
logging.getLogger("").handlers = []
logging.basicConfig(format="%(asctime)s %(message)s", level=log_level)


def bootstrap(name="MicroService", *args, **kwargs):
    list_openapi = Util.load_oai(
        os.getenv(
            "OPENAPI_MULTIPLE_FILES",
            "../../layer2_use_cases/interface_port_file_storage.yml"
        )
    )

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        # TODO: enable validator for response
        app.add_api(
            oai,
            resolver=MultipleResourceResolver(
                "api", collection_endpoint_name="index"),
            validate_responses=False,
        )

    return app


app = bootstrap("PortOwncloud", all=True)