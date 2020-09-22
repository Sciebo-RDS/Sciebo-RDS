import logging
import os
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort
from lib.Util import require_api_key

logger = logging.getLogger()


@require_api_key
def index():
    req = request.json.get("metadata")

    depoResponse = g.osf.get_deposition(metadataFilter=req)
    return jsonify(
        [
            {"projectId": str(depo["prereserve_doi"]["recid"]), "metadata": depo}
            for depo in depoResponse
        ]
    )


@require_api_key
def get(project_id):
    req = request.json.get("metadata")

    depoResponse = g.osf.get_deposition(id=int(project_id), metadataFilter=req)

    return jsonify(depoResponse)


@require_api_key
def post():
    req = request.json.get("metadata")

    depoResponse = g.osf.create_new_deposition_internal(
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
    if g.osf.remove_deposition_internal(int(project_id)):
        return "", 204

    abort(404)


@require_api_key
def patch(project_id):
    req = request.get_json(force=True, cache=True).get("metadata")

    depoResponse = g.osf.change_metadata_in_deposition_internal(
        deposition_id=int(project_id), metadata=req, return_response=True
    )

    if depoResponse.status_code == 200:
        return jsonify(depoResponse.json().get("metadata"))

    abort(depoResponse.status_code)


@require_api_key
def put(project_id):
    if g.osf.publish_deposition_internal(deposition_id=int(project_id)):
        return True, 200

    abort(400)
