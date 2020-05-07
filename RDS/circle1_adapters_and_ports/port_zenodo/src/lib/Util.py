from functools import wraps
from lib.upload_zenodo import Zenodo
from flask import request, g, current_app, abort
import os
import requests
import logging

logger = logging.getLogger()


def loadAccessToken(userId: str, service: str) -> str:
    # FIXME make localhost dynamic for pactman
    tokenStorageURL = os.getenv(
        "USE_CASE_SERVICE_TOKEN_SERVICE", "http://localhost:3000")
    # load access token from token-storage
    result = requests.get(
        f"{tokenStorageURL}/user/{userId}/service/{service}")

    if result.status_code > 200:
        return None

    access_token = result.json()
    logger.debug(f"got: {access_token}")

    if "type" in access_token and access_token["type"].endswith("Token"):
        access_token = access_token["data"]["access_token"]

    logger.debug("userId: {}, token: {}, service: {}".format(
        userId, access_token, service))

    return access_token


def require_api_key(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        g.zenodo = None

        try:
                req = request.get_json(force=True)
                apiKey = req["apiKey"]
        except:
            req = request.form.to_dict()

        logger.debug("req data: {}".format(req))

        try:
            apiKey = req.get("apiKey")

            if apiKey is None:
                apiKey = loadAccessToken(req.get("userId"), "Zenodo")

        except:
            apiKey = None

        if apiKey is None:
            logger.error("apiKey or userId not found.")
            abort(401)

        logger.debug("found apiKey")
        g.zenodo = Zenodo(apiKey, address=current_app.zenodo_address)

        return api_method(*args, **kwargs)

    return check_api_key
