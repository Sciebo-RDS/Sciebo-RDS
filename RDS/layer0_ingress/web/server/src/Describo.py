import os
import requests
from flask import session
from .app import app, domains_dict
import base64
import json


def getSessionId(access_token=None, folder=None, metadataProfile=None):
    informations = session["informations"]
    default = "{}/remote.php/dav".format(os.getenv(
        "OWNCLOUD_URL", "http://localhost:8000")
    )

    _, _, servername = informations["cloudID"].rpartition("@")

    # If the EFSS (OwnCloud / NextCloud) is running locally within the k8s environment,
    # (probably under minikube and without a public IP)
    # we need to access its webdav endpoint through an internal URL.
    webdav_url = None
    if servername is not None:
        server_info = domains_dict.get(servername.replace('.', '-'))
        if server_info is not None and 'INTERNAL_ADDRESS' in server_info:
            webdav_url = server_info['INTERNAL_ADDRESS'] + '/remote.php/dav'

        if webdav_url is None:
            webdav_url = "https://{}/remote.php/dav".format(servername)

    data = {
        # needs to be UID, because webdav checks against UID
        "user_id": informations["UID"],
        "url": webdav_url or default,
    }

    if access_token is not None:
        data["access_token"] = access_token

    if folder is not None and isinstance(folder, str):
        data["folder"] = folder

    if metadataProfile is not None and metadataProfile is not "":
        metadataProfile = {
            "inline": json.loads(base64.b64decode(metadataProfile).decode('utf-8'))
        }
    else:
        metadataProfile = {
            "file": "type-definitions.json",
        }

    payload = {
        "email": informations["email"],
        "name": informations["cloudID"],
        "service": {
            "owncloud": data
        },
        "profile": metadataProfile,
        "configuration": {
                            "allowProfileChange": False,
                            "allowServiceChange": False,
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
