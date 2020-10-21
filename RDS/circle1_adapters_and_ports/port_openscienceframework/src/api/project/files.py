import logging
import os
from lib.Util import require_api_key
from flask import jsonify, request, g, abort
from io import BytesIO

logger = logging.getLogger()


# FIXME: all endpoints need server tests, but POST cannot currently be tested through pactman, because it only supports json as content type
@require_api_key
def index(project_id):
    return jsonify(g.osf.project(project_id).storage().files)


@require_api_key
def get(project_id, file_id):
    fileslist = list(g.osf.project(project_id).storage().files)
    return jsonify(fileslist[file_id])


@require_api_key
def post(project_id):
    logger.debug("Read file from request")
    file = request.files["file"]

    req = request.form.to_dict()
    filename = req["filename"]
    logger.debug("file: {}, filename: {}".format(file, filename))

    logger.debug("Start file upload")
    resp = (
        g.osf.project(project_id)
        .storage()
        .create_file(filename, BytesIO(file.read()), force=True)
    )

    logger.debug("Finished file upload")

    if resp:
        return jsonify({"success": True}), 200

    else:
        raise ValueError("Upload failed.")


@require_api_key
def patch(project_id, file_id):
    raise NotImplementedError()


@require_api_key
def delete(project_id, file_id=None):
    if file_id is None:
        try:
            for file in g.osf.project(project_id).storage().files:
                file.remove()

            return "", 200
        except:
            return abort(500)

    raise NotImplementedError()
