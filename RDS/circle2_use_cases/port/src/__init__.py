import Util as ServerUtil

import logging, os

from RDS import Util as CommonUtil


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


log_level = os.environ.get("LOGLEVEL", "DEBUG")
logger = logging.getLogger("")
logging.getLogger("").handlers = []
logging.basicConfig(format="%(asctime)s %(message)s", level=log_level)


def bootstrap(name="MicroService", *args, **kwargs):
    import os
    from connexion_plus import App, MultipleResourceResolver, Util

    from lib.TokenService import TokenService

    list_openapi = Util.load_oai("use-case_port.yml")

    if "testing" in kwargs:
        ServerUtil.tokenService = TokenService(kwargs["testing"])
        del kwargs["testing"]
    else:
        ServerUtil.tokenService = TokenService()

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        app.add_api(
            oai,
            resolver=MultipleResourceResolver("api", collection_endpoint_name="index"),
            validate_responses=True,
        )

    app.app.json_encoder = CommonUtil.get_encoder()
    monkeypatch()
    
    return app
