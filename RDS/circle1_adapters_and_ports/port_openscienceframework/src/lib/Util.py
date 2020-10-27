from functools import wraps
from flask import request, g, current_app, abort
from osfclient import OSF
import os
import requests
import logging
from pyld import jsonld
import json

logger = logging.getLogger()


def loadAccessToken(userId: str, service: str) -> str:
    # FIXME make localhost dynamic for pactman
    tokenStorageURL = os.getenv(
        "USE_CASE_SERVICE_PORT_SERVICE", "http://localhost:3000"
    )
    # load access token from token-storage
    result = requests.get(
        f"{tokenStorageURL}/user/{userId}/service/{service}",
        verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
    )

    if result.status_code > 200:
        return None

    access_token = result.json()
    logger.debug(f"got: {access_token}")

    if "type" in access_token and access_token["type"].endswith("Token"):
        access_token = access_token["data"]["access_token"]

    logger.debug(
        "userId: {}, token: {}, service: {}".format(userId, access_token, service)
    )

    return access_token


def require_api_key(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        g.zenodo = None

        try:
            req = request.get_json(force=True, cache=True)
        except:
            req = request.form.to_dict()

        apiKey = req.get("apiKey")
        userId = req.get("userId")

        logger.debug("req data: {}".format(req))

        if apiKey is None and userId is not None:
            apiKey = loadAccessToken(userId, "Openscienceframework")

        if apiKey is None:
            logger.error("apiKey or userId not found.")
            abort(401)

        logger.debug("found apiKey")
        g.osf = OSF(
            token=apiKey,
            address=os.getenv(
                "OPENSCIENCEFRAMEWORK_API_ADDRESS", "https://api.test.osf.io/v2"
            ),
        )

        return api_method(*args, **kwargs)

    return check_api_key


def from_jsonld(req):
    logger.debug("before transformation data: {}".format(req))

    try:
        frame = json.load(open("src/lib/fosf.jsonld"))
    except:
        frame = json.load(open("lib/fosf.jsonld"))

    logger.debug("used frame: {}".format(frame))

    done = jsonld.frame(req, frame)
    logger.debug("after framing data: {}".format(done))

    done["title"] = done["name"]
    del done["name"]

    done["description"] = done["description"].replace("\n", " ")

    try:
        del done["@context"]
        del done["@id"]
        del done["@type"]
    except:
        pass

    data = {"data": {"type": "nodes", "attributes": done}}

    logger.debug("after transformation data: {}".format(data))

    return data
