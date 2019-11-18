from connexion_plus import App, MultipleResourceResolver

import logging, os, requests, yaml
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory


log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

def load_yaml_file():
    logger.info("--- Loading OpenAPI file. ---")
    openapi_filepath = os.getenv("OPENAPI_FILEPATH", "openapi.yaml")

    if not os.path.exists(openapi_filepath): # yaml file not exists equals first start
        # no openapi file found. Something was wrong in the container building process
        download_path = os.getenv("OPENAPI_FILEPATH_EXTERNAL", "")
        logger.warning("No openapi file found. Filepath: {}. Download File: {}".format(openapi_filepath, download_path))
        openapi_file = requests.get(download_path)
        openapi_dict = yaml.full_load(openapi_file.content)
        
        with open(openapi_filepath, "w") as file:
            logger.info("dump openapi file")
            file.write(openapi_file.text)
    else:
        logger.info("openapi file found. Filepath: {}".format(openapi_filepath))
        with open(openapi_filepath, 'r') as file:
            logger.info("load openapi file")
            openapi_dict = yaml.full_load(file.read())
    logger.info("--- Loading OpenAPI file finished. ---")

    return openapi_dict

def bootstrap(name='MicroService'):
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

    app = App(name, use_tracer=config.initialize_tracer(), use_metric=True, use_optimizer=True, use_cors=True)
    app.add_api(openapi_dict, resolver=MultipleResourceResolver('api'))

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app

    split = openapi_dict["servers"][0]["url"].split(":")
    port = int(split[-1])

    app.run(port=port, server='gevent')


if __name__ == "__main__":
    bootstrap("PortZenodo")
