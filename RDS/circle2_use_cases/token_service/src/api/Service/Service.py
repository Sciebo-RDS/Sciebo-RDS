from lib.TokenService import TokenService
from flask import jsonify


def index():
    return jsonify(TokenService().getAllOAuthURIForService())


def get(servicename):
    return jsonify(TokenService().getOAuthURIForService(servicename))
