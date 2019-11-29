from flask import jsonify, request
import Util
from lib.User import User
import logging

def index():
    return jsonify(Util.storage.getUsers())


def get(user_id):
    pass

def post(user_id = None):
    if user_id:
        pass

    user = User.from_json(request.json)
    Util.storage.addUser(user)