
""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from json import JSONEncoder, JSONDecoder


def to_default(self, obj):
    return getattr(obj.__class__, "to_json", to_default.default)(obj)


to_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = to_default  # Replace it.

from connexion_plus import App, MultipleResourceResolver, Util

import logging
import os
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

log_level = logging.DEBUG
logger = logging.getLogger('')
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


def monkeypatch():
    """ Module that monkey-patches json module when it's imported so
    JSONEncoder.default() automatically checks for a special "to_json()"
    method and uses it to encode the object if found.
    """
    from json import JSONEncoder, JSONDecoder

    def to_default(self, obj):
        return getattr(obj.__class__, "to_json", to_default.default)(obj)

    to_default.default = JSONEncoder.default  # Save unmodified default.
    JSONEncoder.default = to_default  # Replace it.


def bootstrap(name='MicroService', *args, **kwargs):
    list_openapi = Util.load_oai(
        os.getenv("OPENAPI_FILEPATH", "use-case_exporter.yml"))

    zenodo_address = None
    if "address" in kwargs:
        zenodo_address = kwargs["address"]
        del kwargs["address"]

    app = App(name, *args, **kwargs)


    if zenodo_address is not None:
        app.zenodo_address = zenodo_address

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"), validate_responses=True)

    return app


monkeypatch()
app = bootstrap("UseCaseExporter", all=True)
