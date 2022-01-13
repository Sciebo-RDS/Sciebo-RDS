from flask import jsonify, request, Response
import json

from RDS import BaseService, LoginService, OAuth2Service, Util
from RDS.ServiceException import (
    ServiceExistsAlreadyError,
    ServiceNotExistsError,
)
from werkzeug.exceptions import abort
import logging
import utility

logger = logging.getLogger(__name__)

init_object = Util.try_function_on_dict(
    [OAuth2Service.from_dict, LoginService.from_dict,
        Util.initialize_object_from_json]
)


def index():
    services = utility.storage.getServices()
    data = {"length": len(services), "list": services}

    return jsonify(data)


def get(servicename: str):
    servicename = servicename.lower()
    svc = utility.storage.getService(servicename)
    if svc is not None:
        return jsonify(svc)

    raise ServiceNotExistsError(BaseService(servicename=servicename))


def post():
    data = request.json
    logger.debug("got: {}".format(data))
    svc = Util.getServiceObject(data)

    try:
        utility.storage.addService(svc)

    except ServiceExistsAlreadyError:
        return jsonify({"success": False, "message": "ServiceExistsAlreadyError"}), 200
    except:
        return jsonify({"success": False, "message": "BadRequest"}), 400

    return jsonify({"success": True})


def delete(servicename: str):
    output = False
    try:
        output = utility.storage.removeService(servicename)
    except:
        pass

    return jsonify({"success": output})
