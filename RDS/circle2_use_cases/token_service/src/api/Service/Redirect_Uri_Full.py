from lib.token_storage import TokenStorage
from flask import jsonify

def index(servicename):
    return jsonify(TokenStorage().getOAuthURIForServiceShort(servicename))
