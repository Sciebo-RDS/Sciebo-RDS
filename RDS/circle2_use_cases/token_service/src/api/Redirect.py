from flask import request, redirect
from lib.TokenService import TokenService
import jwt
import os
import requests
from jwt.exceptions import InvalidSignatureError
import Util
import logging
from lib.Exceptions.ServiceExceptions import CodeNotExchangeable

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)

logger = logging.getLogger()


def index():
    if "code" not in request.args or "state" not in request.args:
        return redirect("/authorization_cancel")

    code = request.args.get("code")
    state = request.args.get("state")

    # use state for servicename
    data = None

    try:
        data = jwt.decode(state, TokenService().secret, algorithms="HS256")

        TokenService().exchangeAuthCodeToAccessToken(
            code, data["servicename"], data["refresh_url"])

        return redirect("/authorization_success")

    except Exception as e:
        logger.error(e)
        return redirect("/authorization_cancel")
