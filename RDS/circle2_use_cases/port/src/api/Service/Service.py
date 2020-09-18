from flask import jsonify
import Util
from connexion_plus import FlaskOptimize


def index():
    return jsonify(Util.tokenService.getAllServices())


def get(servicename):
    return jsonify(Util.tokenService.getService(servicename))
