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
            req = request.get_json(force=True)
        except Exception as e:
            logger.error(e, exc_info=True)
            req = request.form.to_dict()

        apiKey = req.get("apiKey")
        userId = req.get("userId")

        logger.debug("req data: {}".format(req))

        if apiKey is None and userId is not None:
            apiKey = loadAccessToken(userId, "Zenodo")

        if apiKey is None:
            logger.error("apiKey or userId not found.")
            abort(401)

        logger.debug("found apiKey")
        g.zenodo = Zenodo(apiKey, address=current_app.zenodo_address)

        return api_method(*args, **kwargs)

    return check_api_key


zenodo_to_jsonld = {
    "title": "https://schema.org/title",
    "description": "https://schema.org/description",
    "tags": "https://schema.org/keywords",
    "access_right": "https://schema.org/publicAccess",
    "publication_date": "https://schema.org/datePublished",
    "id": "https://schema.org/identifier",
    "zenodocategory": "https://www.research-data-services.org/jsonld/zenodocategory",
    "license": "https://schema.org/license",
    "doi": "https://www.research-data-services.org/jsonld/doi",
    "creators": "https://schema.org/creator",
    "affiliation": "https://schema.org/affiliation",
    "name": "https://schema.org/name",
}


def to_jsonld(metadata):
    def parse_creator(user):
        output = {}
        errors = False

        parameterlist = [
            ("affiliation"),
            ("name"),
        ]
        for parameter in parameterlist:
            try:
                output[zenodo_to_jsonld[parameter]] = creator[parameter]
            except KeyError as e:
                logger.error(e)
                errors = True

        return output

    try:
        zenodocategory = "{}/{}".format(
            metadata["upload_type"], metadata["{}_type".format(metadata["upload_type"])]
        )
    except:
        zenodocategory = metadata["upload_type"]

    creators = []

    for creator in metadata["creators"]:
        creators.append(parse_creator(creator))

    jsonld = {zenodo_to_jsonld["creators"]: creators}

    if zenodocategory is not None:
        jsonld[zenodo_to_jsonld["zenodocategory"]] = zenodocategory

    parameterlist = [
        ("title"),
        ("description"),
        ("doi", ["prereserve_doi", "doi"]),
        ("id", ["prereserve_doi", "recid"]),
        ("publication_date"),
        ("license"),
    ]

    for parameter in parameterlist:
        try:
            left, right = parameter
            data = metadata

            for attr in right:
                data = data[attr]

            jsonld[zenodo_to_jsonld[left]] = data
        except:
            try:
                jsonld[zenodo_to_jsonld[parameter]] = metadata[parameter]
            except KeyError as e:
                logger.debug("key {} not found.".format(e))

    try:
        publicAccess = metadata["access_right"] == "open"
        jsonld[zenodo_to_jsonld["access_right"]] = publicAccess
    except:
        jsonld[zenodo_to_jsonld["access_right"]] = True

    return jsonld


from pyld import jsonld
import json


def from_jsonld(jsonld_data):
    try:
        frame = json.load(open("src/lib/fzenodo.jsonld"))
    except:
        frame = json.load(open("lib/fzenodo.jsonld"))

    logger.debug("before transformation data: {}".format(jsonld_data))
    data = jsonld.frame(jsonld_data, frame)
    logger.debug("after framing: {}".format(data))

    data["title"] = data["name"]
    del data["name"]

    data["creators"] = []

    data["publication_date"] = data[zenodo_to_jsonld["publication_date"]]
    del data[zenodo_to_jsonld["publication_date"]]

    for creator in data["creator"]:
        try:
            del creator["@id"]
            del creator["@type"]
        except Exception as e:
            logger.error(e, exc_info=True)

        try:
            creator["affiliation"] = creator["affiliation"]["name"]
        except Exception as e:
            del creator["affiliation"]
            logger.error(e, exc_info=True)

        data["creators"].append(creator)

    del data["creator"]

    if data["zenodocategory"].find("/") > 0:
        typ, subtyp = tuple(data["zenodocategory"].split("/", 1))
        data["upload_type"] = typ
        data["{}_type".format(typ)] = subtyp
        del data["zenodocategory"]

    try:
        del data["@context"]
        del data["@id"]
        del data["@type"]
    except:
        pass

    logger.debug("after transformation data: {}".format(data))

    data["description"] = data["description"].replace("\n", "<br>")

    return data

