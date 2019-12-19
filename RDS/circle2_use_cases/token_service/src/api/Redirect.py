from flask import request, redirect
import Util
import jwt
import os
import requests
from jwt.exceptions import InvalidSignatureError
import Util
import logging
from lib.Exceptions.ServiceException import CodeNotExchangeable
from lib.Service import OAuth2Service
from connexion_plus import FlaskOptimize

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)

logger = logging.getLogger()
def getURL():
    string = request.url
    return "/" + "/".join(string.split("/")[3:-1])

@FlaskOptimize.do_not_minify()
def index():
    if "code" not in request.args or "state" not in request.args:
        url =  getURL() + "/authorization_cancel"
        return redirect(url)

    code = request.args.get("code")
    state = request.args.get("state")

    # use state for servicename
    data = None

    try:
        logger.info(data)
        data = jwt.decode(state, Util.tokenService.secret, algorithms="HS256")

        logger.info(data)

        Util.tokenService.exchangeAuthCodeToAccessToken(
            code, data["servicename"])

        url =  getURL() + "/authorization_success"
        return redirect(url)

    except Exception as e:
        logger.error(str(e))
        url =  getURL() + "/authorization_cancel"
        return redirect(url)
