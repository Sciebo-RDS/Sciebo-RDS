from lib.token_storage import TokenStorage
from flask import jsonify


def index():
    pass


def get(servicename):
    return jsonify(TokenStorage().getOAuthURIForService(servicename))
