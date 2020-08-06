import Util as ServerUtil

import logging, os

from RDS import Util as CommonUtil

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

    CommonUtil.monkeypatch()

    return app
