import Util as ServerUtil


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
    import logging
    import os
    from connexion_plus import App, MultipleResourceResolver, Util

    from lib.TokenService import TokenService

    list_openapi = Util.load_oai(
        os.getenv("OPENAPI_FILEPATH", "use-case_token-storage.yml"))

    if "storage_address" in kwargs:
        ServerUtil.tokenService = TokenService(kwargs["storage_address"])
        del kwargs["storage_address"]
    else:
        ServerUtil.tokenService = TokenService()

    app = App(name, *args, **kwargs)

    for oai in list_openapi:
        app.add_api(oai, resolver=MultipleResourceResolver(
            'api', collection_endpoint_name="index"), validate_responses=True)

    return app

monkeypatch()