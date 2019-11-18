import os
import requests
import logging
from lib.upload_zenodo import Zenodo
from flask import jsonify

logger = logging.getLogger('')

z = Zenodo(os.getenv("ZENODO_API_KEY"))

def index():
    return z.get_deposition()

def get(deposition_id):
    return z.get_deposition(deposition_id)

def put(deposition_id):
    return "deposit update {}".format(deposition_id), 200

def post():
    return z.create_new_deposition(return_response=True).json()

def delete(deposition_id):
    return z.remove_deposition(deposition_id)
