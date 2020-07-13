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
            "../../circle2_use_cases/interface_port_metadata.yml;"
            + "../../circle3_central_services/interface_port_token_storage.yml",
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


def register_service(
    servicename: str,
    authorize_url: str,
    refresh_url: str,
    client_id: str,
    client_secret: str,
):
    tokenStorage = os.getenv("CENTRAL_SERVICE_TOKEN_STORAGE")
    if tokenStorage is None:
        return False

    data = {
        "servicename": servicename,
        "authorize_url": authorize_url,
        "refresh_url": refresh_url,
        "client_id": client_id,
        "client_secret": client_secret,
        "implements": ["metadata"],
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"{tokenStorage}/service",
        json=data,
        headers=headers,
        verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
    )

    if response.status_code != 200:
        raise Exception(
            "Cannot find and register Token Storage, msg:\n{}".format(response.text)
        )

    response = response.json()
    if response["success"]:
        logger.info(f"Registering {servicename} in token storage was successful.")
        return True

    logger.error(
        f"There was an error while registering {servicename} to token storage.\nJSON: {response}"
    )

    return False


app = bootstrap("PortZenodo", all=True)
