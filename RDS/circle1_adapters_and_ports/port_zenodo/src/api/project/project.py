import logging
import os
from lib.upload_zenodo import Zenodo
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort
from lib.Util import require_api_key

logger = logging.getLogger()

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

        parameterlist = [
            ("affiliation"),
            ("name"),
        ]
        for parameter in parameterlist:
            try:
                output[zenodo_to_jsonld[parameter]] = creator[parameter]
            except KeyError as e:
                logger.error(e)

        return output

    try:
        zenodocategory = "{}/{}".format(
            metadata["upload_type"], "{}_type".format(metadata["upload_type"])
        )
    except:
        zenodocategory = metadata["upload_type"]

    metadata["zenodocategory"] = zenodocategory

    creators = []

    for creator in metadata["creators"]:
        creators.append(parse_creator(creator))

    jsonld = {zenodo_to_jsonld["creators"]: creators}

    parameterlist = [
        ("title"),
        ("description"),
        ("doi", ["prereserve_doi", "doi"]),
        ("id", ["prereserve_doi", "recid"]),
        ("access_right"),
        ("publication_date"),
        ("zenodocategory"),
        ("license")
    ]

    for parameter in parameterlist:
        try:
            left, right = parameter
            data = metadata

            for attr in right:
                data = data[attr]

            jsonld[zenodo_to_jsonld[left]] = data
        except:
            jsonld[zenodo_to_jsonld[parameter]] = metadata[parameter]

    jsonld[zenodo_to_jsonld["access_right"]] = (
        jsonld[zenodo_to_jsonld["access_right"]] == "open",
    )

    return jsonld


@require_api_key
def index():
    req = request.json.get("metadata")

    depoResponse = g.zenodo.get_deposition(metadataFilter=req)
    logger.debug("depo response: {}".format(depoResponse))

    try:
        output = []
        for depo in depoResponse:
            output.append(
                {
                    "projectId": str(depo["prereserve_doi"]["recid"]),
                    "metadata": to_jsonld(depo),
                }
            )

    except Exception as e:
        logger.error(e, exc_info=True)

        output = []
        for depo in depoResponse:
            output.append(
                {"projectId": str(depo["prereserve_doi"]["recid"]), "metadata": depo}
            )

    return jsonify(output)


@require_api_key
def get(project_id):
    req = request.json.get("metadata")

    depoResponse = g.zenodo.get_deposition(id=int(project_id), metadataFilter=req)

    logger.debug("depo reponse: {}".format(depoResponse))

    output = depoResponse
    try:
        output["metadata"] = to_jsonld(depoResponse["metadata"])

    except Exception as e:
        logger.error(e, exc_info=True)

    logger.debug("output: {}".format(output))

    return jsonify(output)


@require_api_key
def post():
    req = request.json.get("metadata")

    depoResponse = g.zenodo.create_new_deposition_internal(
        metadata=req, return_response=True
    )

    if depoResponse.status_code < 300:
        depoResponse = depoResponse.json()
        return jsonify(
            {
                "projectId": str(depoResponse.get("id")),
                "metadata": depoResponse.get("metadata"),
            }
        )

    abort(depoResponse.status_code)


@require_api_key
def delete(project_id):
    if g.zenodo.remove_deposition_internal(int(project_id)):
        return "", 204

    abort(404)


@require_api_key
def patch(project_id):
    req = request.get_json(force=True, cache=True).get("metadata")

    depoResponse = g.zenodo.change_metadata_in_deposition_internal(
        deposition_id=int(project_id), metadata=req, return_response=True
    )

    if depoResponse.status_code == 200:
        return jsonify(depoResponse.json().get("metadata"))

    abort(depoResponse.status_code)


@require_api_key
def put(project_id):
    if g.zenodo.publish_deposition_internal(deposition_id=int(project_id)):
        return True, 200

    abort(400)
