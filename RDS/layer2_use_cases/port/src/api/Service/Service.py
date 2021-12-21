from flask import jsonify
import Util
from connexion_plus import FlaskOptimize


def index():
    return jsonify(Util.tokenService.getAllServices(informations=True))


def get(servicename):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    return jsonify(Util.tokenService.getService(servicename, informations=True))
