import json
from RDS import ROParser
import logging
import os
from lib.upload_zenodo import Zenodo
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort
from lib.Util import require_api_key, to_jsonld, from_jsonld

logger = logging.getLogger()


@require_api_key
def index():
    req = request.json.get("metadata")

    depoResponse = g.zenodo.get_deposition(metadataFilter=req)
    logger.debug("depo response: {}".format(depoResponse))

    output = []
    for depo in depoResponse:
        try:
            metadata = to_jsonld(depo)

        except Exception as e:
            logger.error(e, exc_info=True)
            metadata = depo

        output.append({
            "projectId": str(depo["prereserve_doi"]["recid"]),
            "metadata": metadata
        })

    return jsonify(output)


@require_api_key
def get(project_id):
    req = request.json.get("metadata")

    depoResponse = g.zenodo.get_deposition(
        id=int(project_id), metadataFilter=req)

    logger.debug("depo reponse: {}".format(depoResponse))

    output = depoResponse
    try:
        output = to_jsonld(depoResponse.get("metadata") or depoResponse)

    except Exception as e:
        logger.error(e, exc_info=True)
        output = depoResponse

    logger.debug("output: {}".format(output))

    return jsonify(output)


def zenodo(res):
    result = {}

    result["title"] = res["name"]
    result["description"] = res["description"]
    creator = res["creator"]
    result["publication_date"] = res["datePublished"]

    creator = []

    if not isinstance(res["creator"], list):
        res["creator"] = [res["creator"]]

    for c in res["creator"]:
        if isinstance(c, str):
            creator.append({
                "name": c
            })
        else:
            creator.append(c)

    result["creators"] = creator

    if res["zenodocategory"].find("/") > 0:
        typ, subtyp = tuple(res["zenodocategory"].split("/", 1))
        result["upload_type"] = typ
        result["{}_type".format(typ)] = subtyp

    return result


@require_api_key
def post():
    try:
        req = request.get_json(force=True)
        metadata = req.get("metadata")

        logger.debug(f"got metadata: {metadata}")

        if metadata is not None:
            try:
                doc = ROParser(metadata)
                metadata = zenodo(doc.getElement(
                    doc.rootIdentifier, expand=True, clean=True))
            except Exception as e:
                logger.error(e, exc_info=True)

        logger.debug("send metadata: {}".format(metadata))

        depoResponse = g.zenodo.create_new_deposition_internal(
            metadata=metadata, return_response=True
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
    except Exception as e:
        logger.error(e, exc_info=True)
        abort(500)


@require_api_key
def delete(project_id):
    if g.zenodo.remove_deposition_internal(int(project_id)):
        return "", 204

    abort(404)


@require_api_key
def patch(project_id):
    req = request.get_json(force=True)
    logger.debug("request data: {}".format(req))

    metadata = req.get("metadata")
    if metadata is not None:
        try:
            doc = ROParser(metadata)
            metadata = zenodo(doc.getElement(
                doc.rootIdentifier, expand=True, clean=True))
        except Exception as e:
            logger.error(e, exc_info=True)

    userId = req.get("userId")
    logger.debug("transformed data: {}".format(metadata))

    depoResponse = g.zenodo.change_metadata_in_deposition_internal(
        deposition_id=int(project_id), metadata=metadata, return_response=True
    )

    if depoResponse.status_code == 200:
        output = depoResponse.json()

        logger.debug("output: {}".format(output))

        try:
            output["metadata"] = to_jsonld(output["metadata"])

        except Exception as e:
            logger.error(e, exc_info=True)

        logger.debug("finished output: {}".format(output))

        return jsonify(output["metadata"])

    abort(depoResponse.status_code)


@require_api_key
def put(project_id):
    if g.zenodo.publish_deposition_internal(deposition_id=int(project_id)):
        return True, 200

    abort(400)
