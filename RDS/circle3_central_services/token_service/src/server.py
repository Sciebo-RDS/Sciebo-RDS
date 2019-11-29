from connexion_plus import App, MultipleResourceResolver, Util

import logging, os
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory


log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def bootstrap(name='MicroService', executes=True):
    config = jConfig(
        config={  # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=name,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(namespace=name),
    )

    list_openapi = Util.load_oai(os.getenv("OPENAPI_FILEPATH", "central-service_token-storage.yml"))

    app = App(name, use_tracer=config.initialize_tracer(),
              use_metric=True, use_optimizer={"compress": False, "minify": False}, use_cors=True)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"))

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app

    if executes:
        app.run(port=8080, server='gevent')

    # return app for test or error handling purpose
    return app


if __name__ == "__main__":
    bootstrap("PortZenodo")
