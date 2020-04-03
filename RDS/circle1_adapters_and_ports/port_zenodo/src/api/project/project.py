import logging
import os
from lib.upload_zenodo import Zenodo
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort

logger = logging.getLogger()


def index():
    req = request.json.get("metadata")

    depoResponse = g.zenodo.get_deposition(metadataFilter=req)
    return jsonify(depoResponse)


def get(project_id):
    req = request.json.get("metadata")

    depoResponse = g.zenodo.get_deposition(
        id=int(project_id), metadataFilter=req)

    return jsonify(depoResponse)


def post():
    req = request.json.get("metadata")

    depoResponse = g.zenodo.create_new_deposition_internal(
        metadata=req, return_response=True)

    if depoResponse.status_code < 300:
        return jsonify(depoResponse.json().get("metadata"))

    abort(depoResponse.status_code)


def delete(project_id):
    if g.zenodo.remove_deposition_internal(int(project_id)):
        return "", 200

    abort(404)


def patch(project_id):
    req = request.json.get("metadata")

    depoResponse = g.zenodo.change_metadata_in_deposition_internal(
        deposition_id=int(project_id), metadata=req, return_response=True)

    if depoResponse.status_code == 200:
        return jsonify(depoResponse.json().get("metadata"))

    abort(depoResponse.status_code)
