from connexion_plus import App, MultipleResourceResolver, Util

import logging
import os
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory


log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def bootstrap(name='MicroService', *args, **kwargs):
    list_openapi = Util.load_oai("https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/port_invenio.yml;" +
                                 "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/port_invenio.yml")

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"), validate_responses=True)

    return app


if __name__ == "__main__":
    app = bootstrap("PortZenodo", all=True)

    # TODO: Register service at token storage

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    app.run(port=8080, server='gevent')
