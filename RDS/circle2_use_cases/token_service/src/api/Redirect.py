from flask import request, redirect
from lib.TokenService import TokenService
import jwt
import os
import requests
from jwt.exceptions import InvalidSignatureError
import Util, logging
from lib.Exceptions.ServiceExceptions import CodeNotExchangeable

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)

logger = logging.getLogger()

def index():
    code = None
    if "code" in request.args:
        code = request.args.get("code")

    state = None
    if "state" in request.args:
        state = request.args.get("state")

    if code is None or state is None:
        return redirect("/authorization_cancel")

    # use state for servicename
    data = None
    try:
        data = jwt.decode(state, TokenService().secret, algorithms="HS256")
    except InvalidSignatureError:
        return redirect("/authorization_cancel")

    
    try:
        TokenService().exchangeAuthCodeToAccessToken(code, data["servicename"], data["refresh_url"])
        return redirect("/authorization_success")
    except CodeNotExchangeable as e:
        logger.error(e)
        return redirect("/authorization_cancel")

