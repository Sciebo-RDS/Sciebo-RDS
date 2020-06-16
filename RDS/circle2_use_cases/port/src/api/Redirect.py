from flask import request, redirect
import Util
import jwt
import os
import requests
from jwt.exceptions import InvalidSignatureError

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

    code = request.args.get("code")
    state = request.args.get("state")

    # state is base64 for dict:
    # {
    #   "user": <user id for logged user account in interface>, 
    #   "jwt": <state jwt from port-service system>
    # }

    if code is None or state is None:
        url = getURL() + "/authorization-cancel"
        return redirect(url)

    # use state for servicename
    data = None

    try:
        import json
        import base64
        state_dict = json.loads(base64.b64decode(state))
        data = jwt.decode(state_dict.get("jwt"),
                          Util.tokenService.secret, algorithms="HS256")

        logger.debug("code: {}, state: {}".format(code, state))
        logger.debug(f"decoded state: {data}")

        Util.tokenService.exchangeAuthCodeToAccessToken(
            code, Util.tokenService.getService(data["servicename"], clean=True), user=state_dict.get("user"))

        url = getURL() + "/authorization-success"
        return redirect(url)

    except Exception as e:
        logger.exception(e)
        url = getURL() + "/authorization-cancel"
        return redirect(url)
