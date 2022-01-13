import os
import requests
from flask import session
from .app import app


def getSessionId(access_token=None, folder=None):
    informations = session["informations"]
    data = {
        "user_id": informations["UID"],
        "url": "{}/remote.php/dav".format(
            os.getenv("OWNCLOUD_URL", "http://localhost:8000")
        ),
    }

    if access_token is not None:
        data["access_token"] = access_token

    if folder is not None and isinstance(folder, str):
        data["folder"] = folder

    payload = {
        "email": informations["email"],
        "name": informations["name"],
        "session": {
            "owncloud": data
        }
    }

    headers = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer {}".format(os.getenv("DESCRIBO_API_SECRET"))
    }

    app.logger.debug("send payload: {}, headers: {}".format(payload, headers))

    req = requests.post(
        os.getenv("DESCRIBO_API_ENDPOINT"),
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
