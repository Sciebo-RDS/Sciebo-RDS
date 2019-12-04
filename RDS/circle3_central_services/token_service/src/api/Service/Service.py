from flask import jsonify, request, Response
import Util, json

from lib.Service import Service, OAuth2Service
from lib.Exceptions.ServiceExceptions import ServiceExistsAlreadyError
from werkzeug.exceptions import abort

def index():
    return jsonify(Util.storage.getServices())


def get(servicename):
    svc = Util.storage.getService(servicename)
    if svc is not None:
        return jsonify(svc)

    abort(Response(f"{servicename} not found."))
    

def post():
    svc = Util.initialize_object_from_json(request.json)

    try:
        Util.storage.addService(svc)

    except ServiceExistsAlreadyError:
        Util.storage.addService(svc, Force=True)
        return '', 204
    except:
        raise

    return "", 200