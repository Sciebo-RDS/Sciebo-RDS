import logging
import os
from lib.upload_zenodo import Zenodo
from flask import jsonify, request

def index(project_id):

    return jsonify({})


def get(project_id, file_id):

    return jsonify({})


def post(project_id):
    req = request.data

    return jsonify({})


def patch(project_id, file_id):
    req = request.data

    return jsonify({})

def delete(project_id, file_id):
    pass
