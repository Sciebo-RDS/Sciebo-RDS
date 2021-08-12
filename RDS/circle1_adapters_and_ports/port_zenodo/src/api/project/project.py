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


@require_api_key
def post():

    req = request.json.get("metadata")

    try:
        req = from_jsonld(req)
    except:
        pass

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
    req = request.get_json(force=True)

    logger.debug("request data: {}".format(req))
    userId = req.get("userId")
    metadata = req.get("metadata")

    try:
        metadata = from_jsonld(metadata)
    except Exception as e:
        logger.error(e, exc_info=True)

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
