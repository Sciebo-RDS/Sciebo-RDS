from flask import jsonify, request, abort
import json
from . import Util
from lib.User import User
from lib.Exceptions.StorageException import UserHasTokenAlreadyError, UserNotExistsError
from lib.Token import Token, OAuth2Token

init_object = Util.try_function_on_dict([OAuth2Token.from_dict, Token.from_dict, Util.initialize_object_from_json])

def index(user_id):
    try:
        tokens = Util.storage.getTokens(user_id)
    except UserNotExistsError as e:
        abort(404, description=str(e))
    
    data = {
        "length": len(tokens),
        "list": tokens
    }
    return jsonify(data)


def post(user_id):
    token = init_object(request.json)
    try:
        Util.storage.addTokenToUser(token, User(user_id))
    except UserHasTokenAlreadyError as e:
        abort(409, description=str(e))

    return jsonify({"success": True})


def get(user_id, token_id):
    try:
        token = Util.storage.getToken(user_id, int(token_id))
        return jsonify(token)
    except UserNotExistsError as e:
        abort(404, description=str(e))
    except ValueError as e:
        abort(404, description=str(e))


def delete(user_id, token_id):
    user = Util.storage.getUser(user_id)
    token = Util.storage.getToken(user_id, int(token_id))

    Util.storage.removeToken(user, token)
    return jsonify({"success": True})
