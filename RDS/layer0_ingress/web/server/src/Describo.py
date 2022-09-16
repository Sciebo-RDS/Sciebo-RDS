import os
import requests
from flask import session
from .app import app


def getSessionId(access_token=None, folder=None):
    informations = session["informations"]
    default = "{}/remote.php/dav".format(os.getenv(
        "OWNCLOUD_URL", "http://localhost:8000")
    )

    _, _, servername = informations["cloudID"].rpartition("@")

    if servername is not None:
        servername = "https://{}/remote.php/dav".format(servername)

    data = {
        # needs to be UID, because webdav checks against UID
        "user_id": informations["UID"],
        "url": servername or default,
    }

    if access_token is not None:
        data["access_token"] = access_token

    if folder is not None and isinstance(folder, str):
        data["folder"] = folder

    payload = {
        "email": informations["email"],
        "name": informations["cloudID"],
        "session": {
            "owncloud": data
        },
        "profile": {
            "file": "type-definitions.json",
        },
    }

    headers = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer {}".format(os.getenv("DESCRIBO_API_SECRET"))
    }

    app.logger.debug("send payload: {}, headers: {}".format(payload, headers))

    req = requests.post(
        os.getenv("DESCRIBO_API_ENDPOINT", "http://layer0-describo/api/session/application"),
        json=payload,
        headers=headers
    )

    app.logger.debug("response:\nheaders: {}\nbody: {}".format(
        req.headers, req.text))

    describoPayload = {
        "sessionId": req.json().get("sessionId"),
        "payload": payload
    }

    return describoPayload
