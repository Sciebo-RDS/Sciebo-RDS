import logging
import os
from flask import jsonify, request

logger = logging.getLogger('')


def index(deposition_id):
    raise NotImplementedError


def get(deposition_id, creator_id):
    raise NotImplementedError


def put(deposition_id, creator_id=-1):
    raise NotImplementedError


def delete(deposition_id, creator_id):
    raise NotImplementedError
