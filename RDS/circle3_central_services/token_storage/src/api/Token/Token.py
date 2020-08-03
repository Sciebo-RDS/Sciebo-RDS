from flask import jsonify
from RDS import Token, OAuth2Token
import utility


def index():
    tokens = utility.storage.getTokens()
    data = {"length": len(tokens), "list": tokens}
    return jsonify(data)


# TODO Implements me


def get(token_id):
    raise NotImplementedError


def put(token_id):
    raise NotImplementedError


def post():
    raise NotImplementedError
