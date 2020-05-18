
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from jaeger_client import Config as jConfig
import os
import logging
from connexion_plus import App, MultipleResourceResolver, Util
from json import JSONEncoder, JSONDecoder
from gevent import monkey
monkey.patch_all()


log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def monkeypatch():
    """ 
    Module that monkey-patches json module when it's imported so
    JSONEncoder.default() automatically checks for a special "getJSON"
    method and uses it to encode the object if found.
    """
    from json import JSONEncoder, JSONDecoder

    def to_default(self, obj):
        return getattr(obj.__class__, "getJSON", to_default.default)(obj)

    to_default.default = JSONEncoder.default  # Save unmodified default.
    JSONEncoder.default = to_default  # Replace it.


def bootstrap(name='MicroService', *args, **kwargs):
    list_openapi = Util.load_oai("use-case_metadata.yml")

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"), validate_responses=True)

    return app


monkeypatch()
app = bootstrap("UseCaseMetadata", all=True)
