from flask import jsonify, request, abort
import logging
from RDS import Util, User, Token, OAuth2Token
import utility
import json
from lib.Exceptions.StorageException import UserHasTokenAlreadyError, UserNotExistsError

init_object = Util.try_function_on_dict(
    [OAuth2Token.from_dict, Token.from_dict, Util.initialize_object_from_json]
)
logger = logging.getLogger()


def index(user_id):
    try:
        tokens = utility.storage.getTokens(user_id)
    except UserNotExistsError as e:
        abort(404, description=str(e))

    data = {"length": len(tokens), "list": tokens}

    logger.debug(f"Found tokens: {json.dumps(data)}")
    return jsonify(data)


def post(user_id):
    logger.debug(f"get token string: {request.json}.")

    from RDS import Token

    token = Util.getTokenObject(request.json)

    logger.debug(f"parsed token: {token}.")

    code = 200

    try:
        user = utility.storage.getUser(user_id)
    except UserNotExistsError as e:
        user = User(user_id)

    try:
        utility.storage.addTokenToUser(token, user)
    except UserHasTokenAlreadyError as e:
        abort(409, description=str(e))
    except UserNotExistsError as e:
        # only force adding, if user not exists, otherwise it also overwrites existing tokens.
        utility.storage.addTokenToUser(token, user, Force=True)
        code = 201

    return jsonify({"success": True}), code


def put(user_id, token_id):
    try:
        token = utility.storage.getToken(user_id, token_id)

        return {
            "success": utility.storage.internal_refresh_token(token)
        }

    except UserNotExistsError as e:
        abort(404, description=str(e))
    except ValueError as e:
        abort(404, description=str(e))
    except Exception as e:
        logger.error(str(e), exc_info=True)

    abort(500)


def get(user_id, token_id):
    try:
        token = utility.storage.getToken(user_id, token_id)
        return token.to_json()
    except UserNotExistsError as e:
        abort(404, description=str(e))
    except ValueError as e:
        abort(404, description=str(e))


def delete(user_id, token_id):
    user = utility.storage.getUser(user_id)
    token = utility.storage.getToken(user_id, token_id)

    utility.storage.removeToken(user, token)
    return jsonify({"success": True})
