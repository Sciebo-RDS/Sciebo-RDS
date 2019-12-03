from flask import jsonify
import Util

def index():
    data = Util.storage.getTokens()
    return data


def get(token_id):
    pass

def put(token_id):
    pass

def post():
    pass

