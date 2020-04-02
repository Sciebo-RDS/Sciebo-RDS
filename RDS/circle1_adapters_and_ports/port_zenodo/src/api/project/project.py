import logging
import os
from lib.upload_zenodo import Zenodo
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort

logger = logging.getLogger()


def index():
    depoResponse = g.zenodo.get_deposition(return_response=True)

    if depoResponse.status_code < 300:
        resp = depoResponse.json()

        # TODO add filter to resp if request.json["metadata"] is set
        return jsonify(resp)
    
    abort(depoResponse.status_code)


def get(project_id):
    depoResponse = g.zenodo.get_deposition(int(project_id), return_response=True)

    if depoResponse.status_code < 300:
        resp = depoResponse.json()

        # TODO add filter to resp if request.json["metadata"] is set
        return jsonify(resp)
    
    abort(depoResponse.status_code)


def post():
    pass


def delete(project_id):
    pass


def patch(project_id):
    #req = request.json

    pass
