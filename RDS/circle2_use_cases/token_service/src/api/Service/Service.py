from lib.TokenService import TokenService
from flask import jsonify


def index():
    return jsonify(TokenService().getAllServices())


def get(servicename):
    return jsonify(TokenService().getService(servicename))
