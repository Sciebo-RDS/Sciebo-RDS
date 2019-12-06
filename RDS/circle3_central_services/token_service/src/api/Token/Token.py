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


def get(token_id):
    pass

def put(token_id):
    pass

def post():
    pass

def get_token_object(jsonStr):
    try:
        return OAuth2Token.from_dict(request.json)
    except ValueError:
        pass

    try:
        return Token.from_dict(request.json)
    except ValueError:
        pass

    try:
        return Util.initialize_object_from_json(request.json)
    except ValueError:
        pass

    raise ValueError("Cannot interpret given string as service.")