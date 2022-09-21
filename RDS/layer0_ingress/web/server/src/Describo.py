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
        "service": {
            "owncloud": data
        },
        "profile": {
            "inline": {
                "metadata":{
                    "name" : "Test Profile",
                    "description": "a profile to learn writing profiles",
                    "version" : 0.1,
                    "warnMissingProperty" : False
            },
                "classes": {
                "Person": {
                    "definition": "override",
                    "subClassOf": [
                        "Thing"
                    ],
                    "inputs": [
                        {
                            "id": "http://schema.org/address",
                            "name": "address",
                            "help": "Physical address of the item.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        },
                        {
                            "id": "http://schema.org/affiliation",
                            "name": "affiliation",
                            "help": "An organization that this person is affiliated with. For example, a school/university, a club, or a team.",
                            "multiple": False,
                            "type": [
                                "Organization"
                            ]
                        },
                        {
                            "id": "http://schema.org/email",
                            "name": "email",
                            "help": "Email address.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        },
                        {
                            "id": "http://schema.org/familyName",
                            "name": "familyName",
                            "help": "Family name. In the U.S., the last name of a Person.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        },
                        {
                            "id": "http://schema.org/givenName",
                            "name": "givenName",
                            "help": "Given name. In the U.S., the first name of a Person.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        }
                    ]
                },
                "Thing": {
                    "definition": "override",
                    "subClassOf": [],
                    "inputs": [
                        {
                            "id": "http://schema.org/description",
                            "name": "description",
                            "help": "A description of the item.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        },
                        {
                            "id": "http://schema.org/name",
                            "name": "name",
                            "help": "The name of the item.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        }
                    ]
                },
                "Organization": {
                    "definition": "override",
                    "subClassOf": [
                        "Thing"
                    ],
                    "inputs": [
                        {
                            "id": "http://schema.org/address",
                            "name": "address",
                            "help": "Physical address of the item.",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        }
                    ]
                },
                "CreativeWork": {
                    "definition": "override",
                    "subClassOf": [
                        "Thing"
                    ],
                    "inputs": [
                        {
                            "id": "http://schema.org/author",
                            "name": "creator",
                            "help": "The author of this content or rating. Please note that author is special in that HTML 5 provides a special mechanism for indicating authorship via the rel tag. That is equivalent to this and may be used interchangeably. ",
                            "multiple": False,
                            "type": [
                                "Person",
                                "Organization"
                            ]
                        }
                    ]
                },
                "Dataset": {
                    "definition": "override",
                    "subClassOf": [
                        "CreativeWork"
                    ],
                    "inputs": [
                        {
                            "id": "http://schema.org/datePublished",
                            "name": "datePublished",
                            "help": "Date of first broadcast/publication.",
                            "multiple": False,
                            "type": [
                                "Date"
                            ]
                        },
                        {
                            "id": "http://schema.org/zenodocategory",
                            "name": "zenodocategory",
                            "help": "The Zenodo Category: [ 'publication/book', 'publication section', '...', 'dataset', 'image/plot', '...' ]",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        },
                        {
                            "id": "http://schema.org/osfcategory",
                            "name": "osfcategory",
                            "help": "The OSF Category: [ 'analysis', 'communication', '...', 'procedure', 'instrumentation', '...' ]",
                            "multiple": False,
                            "type": [
                                "Text"
                            ]
                        }
                    ]
                }},
                "enabledClasses" : ["Person", "Organization"]
            },
                    },
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
