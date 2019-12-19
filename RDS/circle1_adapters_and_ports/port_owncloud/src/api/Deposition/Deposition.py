import os
import requests
import logging
from flask import jsonify

logger = logging.getLogger('')


def index():
    raise NotImplementedError

def get(deposition_id):
    raise NotImplementedError

def put(deposition_id):
    raise NotImplementedError

def post():
    raise NotImplementedError

def delete(deposition_id):
    raise NotImplementedError
