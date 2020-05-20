from flask import request, redirect, abort
import Util
import json
import jwt
import logging

logger = logging.getLogger()


def post():
    try:
        master_jwt = request.json.get("jwt")
        unverified = jwt.decode(master_jwt, verify=False)

        servicename = unverified.get("servicename")
        service = Util.tokenService.getService(servicename, clean=True)

        master_data = jwt.decode(
            master_jwt, service.client_secret, algorithms="HS256")

        logger.debug("jwt: {}, decoded: {}".format(master_jwt, master_data))

        userId = master_data.get("userId")
        code = master_data.get("code")
        logger.debug("code: {}, userId: {}".format(code, userId))

        state_jwt = master_data.get("state")
        state_data = jwt.decode(
            state_jwt, Util.tokenService.secret, algorithms="HS256")

        logger.debug("state: {}, decoded state: {}".format(
            state_jwt, state_data))

        Util.tokenService.exchangeAuthCodeToAccessToken(
            code, Util.tokenService.getService(state_data["servicename"], clean=True), user=userId)

        return "", 204

    except Exception as e:
        logger.exception(e)

        abort(400)
