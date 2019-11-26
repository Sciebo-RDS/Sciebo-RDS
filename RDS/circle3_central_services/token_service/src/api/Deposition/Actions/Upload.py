import os
from lib.upload_zenodo import Zenodo
from flask import request

z = Zenodo(os.getenv("ZENODO_API_KEY"))

def index(deposition_id):
    # TODO add me
    pass

def post(deposition_id):
    # TODO add me
    pass
