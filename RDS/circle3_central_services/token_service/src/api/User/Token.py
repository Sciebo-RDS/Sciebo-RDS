from flask import jsonify, request, abort
import json
from . import Util
import logging
from lib.User import User
from lib.Exceptions.StorageException import UserHasTokenAlreadyError, UserNotExistsError
from lib.Token import Token, OAuth2Token

init_object = Util.try_function_on_dict([OAuth2Token.from_dict, Token.from_dict, Util.initialize_object_from_json])
logger = logging.getLogger()

def index(user_id):
    try:
        tokens = Util.storage.getTokens(user_id)
    except UserNotExistsError as e:
        abort(404, description=str(e))
    
    data = {
        "length": len(tokens),
        "list": tokens
    }

    logger.debug(f"Found services: {json.dumps(data)}")
    return jsonify(data)


def post(user_id):
    logger.debug(f"get token string: {request.json}.")
    
    from lib.Token import Token
    token = Token.init(request.json)

    logger.debug(f"parsed token: {token}.")

    code = 200
    try:
        Util.storage.addTokenToUser(token, user_id)
    except UserHasTokenAlreadyError as e:
        abort(409, description=str(e))
    except UserNotExistsError as e:
        # only force adding, if user not exists, otherwise it also overwrites existing tokens.
        Util.storage.addTokenToUser(token, user_id, Force=True)
        code = 201

    return jsonify({"success": True}), code


def get(user_id, token_id):
    try:
        token = Util.storage.getToken(user_id, token_id)
        return jsonify(token)
    except UserNotExistsError as e:
        abort(404, description=str(e))
    except ValueError as e:
        abort(404, description=str(e))


def delete(user_id, token_id):
    user = Util.storage.getUser(user_id)
    token = Util.storage.getToken(user_id, token_id)

    Util.storage.removeToken(user, token)
    return jsonify({"success": True})
