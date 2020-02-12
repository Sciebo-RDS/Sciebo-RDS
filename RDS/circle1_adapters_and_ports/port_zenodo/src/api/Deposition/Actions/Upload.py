import os
import logging
from lib.upload_zenodo import Zenodo
from flask import request, jsonify, g
from lib.Util import loadAccessToken

logger = logging.getLogger()


def index(deposition_id):
    # TODO add me
    pass


def post(deposition_id):
    if g.zenodo is None:
        return "No userid provided. Unauthorized access", 401

    file = request.files['file']
    resp = g.zenodo.upload_new_file_to_deposition(deposition_id, file)

    if resp:
        return jsonify({"success": True})
    else:
        raise ValueError("Upload failed.")
