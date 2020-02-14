import os
import requests
import logging
from lib.upload_zenodo import Zenodo
from flask import jsonify, request, g

logger = logging.getLogger()


def index():
    if g.zenodo is None:
        return "No userid provided. Unauthorized access", 401

    logger.debug("get deposition list")
    return g.zenodo.get_deposition()


def get(deposition_id):
    if g.zenodo is None:
        return "No userid provided. Unauthorized access", 401

    return g.zenodo.get_deposition(deposition_id)


def put(deposition_id):
    # TODO implements needed
    # return "deposit update {}".format(deposition_id), 200
    pass


def post():
    if g.zenodo is None:
        return "No userid provided. Unauthorized access", 401

    r = g.zenodo.create_new_deposition(return_response=True)
    return jsonify({"depositionId": r.json()["id"]})


def delete(deposition_id):
    pass
    # return zenodo.remove_deposition(deposition_id)
