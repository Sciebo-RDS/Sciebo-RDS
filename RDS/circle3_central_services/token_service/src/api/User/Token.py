from flask import jsonify, request
import json
from . import Util
from lib.User import User
from lib.Exceptions.StorageException import UserHasTokenAlreadyError
from lib.Token import Token, OAuth2Token

init_object = Util.try_function_on_dict([OAuth2Token.from_dict, Token.from_dict, Util.initialize_object_from_json])

def index(user_id):
    tokens = Util.storage.getTokens(user_id)
    data = {
        "length": len(tokens),
        "list": tokens
    }
    return jsonify(data)


def post(user_id):
    token = init_object(request.json)
    Util.storage.addTokenToUser(token, User(user_id))

    return jsonify({"success": True})


def get(user_id, token_id):
    token = Util.storage.getToken(user_id, int(token_id))
    return jsonify(token)


def delete(user_id, token_id):
    user = Util.storage.getUser(user_id)
    token = Util.storage.getToken(user_id, int(token_id))

    Util.storage.removeToken(user, token)
    return jsonify({"success": True})
