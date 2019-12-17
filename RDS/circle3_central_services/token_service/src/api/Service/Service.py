from flask import jsonify, request, Response
import Util, json

from lib.Service import Service, OAuth2Service
from lib.Exceptions.ServiceException import ServiceExistsAlreadyError, ServiceNotExistsError
from werkzeug.exceptions import abort


init_object = Util.try_function_on_dict([OAuth2Service.from_dict, Service.from_dict, Util.initialize_object_from_json])

def index():
    services = Util.storage.getServices()
    data = {
        "length": len(services),
        "list": services
    }
    return jsonify(data)


def get(servicename: str):
    svc = Util.storage.getService(servicename)
    if svc is not None:
        return jsonify(svc)

    raise ServiceNotExistsError(Service(servicename))    

def post():
    svc = init_object(request.json)

    try:
        Util.storage.addService(svc)

    except ServiceExistsAlreadyError:
        Util.storage.addService(svc, Force=True)
    except:
        raise

    return jsonify({"success": True})
