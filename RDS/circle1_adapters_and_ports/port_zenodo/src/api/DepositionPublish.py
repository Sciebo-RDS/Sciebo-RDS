import os
from lib.upload_zenodo import Zenodo
from flask import request

z = Zenodo(os.getenv("ZENODO_API_KEY"))

def index(deposition_id):
    r = z.get_deposition(return_response=True)
    v = r["submitted"]
    return v, r.status_code

def put(deposition_id):
    r = z.publish_deposition_internal(deposition_id, return_response=True)
    return r.status_code == 202, r.status_code
