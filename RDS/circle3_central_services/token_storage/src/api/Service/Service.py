from flask import jsonify, request, Response
import json

from RDS import Service, OAuth2Service, Util
from RDS.ServiceException import (
    ServiceExistsAlreadyError,
    ServiceNotExistsError,
)
from werkzeug.exceptions import abort
import logging
import utility

logger = logging.getLogger(__name__)

init_object = Util.try_function_on_dict(
    [OAuth2Service.from_dict, Service.from_dict, Util.initialize_object_from_json]
)


def index():
    services = utility.storage.getServices()
    data = {"length": len(services), "list": services}
    return jsonify(data)


def get(servicename: str):
    svc = utility.storage.getService(servicename)
    if svc is not None:
        return jsonify(svc)

    raise ServiceNotExistsError(Service(servicename))


def post():
    data = request.json
    logger.debug("got: {}".format(data))
    svc = Service.init(data)

    try:
        utility.storage.addService(svc)

    except ServiceExistsAlreadyError:
        utility.storage.addService(svc, Force=True)
    except:
        raise

    return jsonify({"success": True})
