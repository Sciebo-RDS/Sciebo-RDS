from flask import request, redirect, abort
import Util
import json
import jwt
import logging
import base64

logger = logging.getLogger()


def post():
    """
    This endpoint implements the same like redirect, but it returns 204 for success and 400 if something goes wrong.
    This enables, that integrations can trigger the serverpart of oauth workflow in rds by themselves.
    """
    try:
        master_jwt = request.json.get("jwt")
        logger.debug("jwt: {}".format(master_jwt))

        unverified = jwt.decode(master_jwt, algorithms="HS256", options={"verify_signature": False})
        logger.debug("unverified: {}".format(unverified))

        servicename = unverified.get("servicename").lower()
        service = Util.tokenService.getService(servicename, clean=True)

        master_data = jwt.decode(master_jwt, service.client_secret, algorithms="HS256")
        logger.debug("verified: {}".format(master_data))

        userId = master_data.get("userId")
        code = master_data.get("code")
        logger.debug("code: {}, userId: {}".format(code, userId))

        stateJWT = master_data.get("state")
        state = jwt.decode(stateJWT, Util.tokenService.secret, algorithms="HS256")

        logger.debug("state: {}, decoded state: {}".format(stateJWT, state))

        Util.tokenService.exchangeAuthCodeToAccessToken(
            code,
            Util.tokenService.getService(state["servicename"], clean=True),
            user=userId,
        )

        return "", 204

    except Exception as e:
        logger.exception(e)

        abort(400)
