from functools import wraps
from flask import request, g, current_app, abort
from osfclient import OSF
import os
import requests
import logging
from pyld import jsonld
import json
from RDS import Util

logger = logging.getLogger()


def require_api_key(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        g.zenodo = None

        try:
            req = request.get_json(force=True, cache=True)
        except:
            req = request.form.to_dict()

        try:
            service, userId, apiKey = Util.parseUserId(req.get("userId"))
        except:
            apiKey = Util.loadToken(req.get("userId"), "Openscienceframework").access_token

        logger.debug("req data: {}".format(req))

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
