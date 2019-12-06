from flask import jsonify
from lib.Token import Token, OAuth2Token
import Util


def index():
    tokens = Util.storage.getTokens()
    data = {
        "length": len(tokens),
        "list": tokens
    }
    return jsonify(data)

# TODO Implements me


def get(token_id):
    raise NotImplementedError


def put(token_id):
    raise NotImplementedError


def post():
    raise NotImplementedError
