from connexion_plus import App, MultipleResourceResolver

import logging
import os
import requests
import yaml
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory


log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def load_yaml_file():
    logger.info("--- Loading OpenAPI file. ---")
    openapi_filepath = os.getenv("OPENAPI_FILEPATH", "openapi.yaml")

    # yaml file not exists equals first start
    openapi_dict = []
    if not os.path.exists(openapi_filepath):
        # no openapi file found. Something was wrong in the container building process
        paths = ["https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/port_invenio.yml",
                 "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/port_invenio.yml"]
        paths = ";".join(paths)

        download_path = os.getenv("OPENAPI_FILEPATH_EXTERNAL", paths)
        logger.warning("No openapi file found. Filepath: {}. Loads webfiles: {}".format(
            openapi_filepath, download_path))

        downloads = download_path.split(";")
        for d in downloads:
            openapi_file = requests.get(d)
            openapi_dict.append(yaml.full_load(openapi_file.content))
    else:
        logger.info("openapi file found. Filepath: {}".format(openapi_filepath))

        with open(openapi_filepath, 'r') as f:
            logger.info("load openapi file")
            openapi_dict.append(yaml.full_load(f.read()))

    logger.info("--- Loading OpenAPI file finished. ---")

    return openapi_dict


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

    openapi_dict = load_yaml_file()

    app = App(name, use_tracer=config.initialize_tracer(),
              use_metric=True, use_optimizer={"compress": False, "minify": False}, use_cors=True)

    for oai in openapi_dict:
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
