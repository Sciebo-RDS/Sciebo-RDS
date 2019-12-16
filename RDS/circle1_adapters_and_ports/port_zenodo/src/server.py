from connexion_plus import App, MultipleResourceResolver, Util

import logging
import os
import json
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
import requests

log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def bootstrap(name='MicroService', *args, **kwargs):
    list_openapi = Util.load_oai(os.getenv("OPENAPI_MULTIPLE_FILES",
                                           "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/port_invenio.yml;" +
                                           "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/port_invenio.yml"))

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"), validate_responses=True)

    return app


def register_service(servicename: str, authorize_url: str, refresh_url: str, client_id: str, client_secret: str):
    tokenStorage = os.getenv("CENTRAL-SERVICE_TOKEN-STORAGE")
    data = {
        "type": "OAuth2Service",
        "data": {
            "servicename": servicename,
            "authorize_url": authorize_url,
            "refresh_url": refresh_url,
            "client_id": client_id,
            "client_secret": client_secret}
    }
    response = requests.post(
        f"{tokenStorage}/service", data=json.dumps(data))

    if response.status_code is not 200:
        raise Exception(
            "Cannot find and register Token Storage, msg:\n{}".format(response.text))

    response = response.json
    if response["success"]:
        logger.info(
            f"Registering {servicename} in token storage was successful.")
        return True

    logger.error(
        f"There was an error while registering {servicename} to token storage.\nJSON: {response}")

    return False


if __name__ == "__main__":
    app = bootstrap("PortZenodo", all=True)

    # TODO: Register service at token storage
    register_service(
        "PortZenodo",
        "ZENODO_OAUTH_AUTHORIZE_URL",
        "ZENODO_OAUTH_ACCESS_TOKEN_URL",
        "ZENODO_OAUTH_CLIEND_ID",
        "ZENODO_OAUTH_CLIENT_SECRET"
    )

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    app.run(port=8080, server='gevent')
