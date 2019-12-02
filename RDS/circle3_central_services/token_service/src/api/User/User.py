from flask import jsonify, request
import Util
from lib.User import User
import logging

def index():
    return jsonify(Util.storage.getUsers())


def get(user_id):
    try:
        return jsonify(Util.storage.getUser(user_id))
    except:
        return "", 404

def post():
    user = User.from_json(request.json)
    Util.storage.addUser(user)
    return "", 200

def delete(user_id):
    try:
        Util.storage.removeUser(User(user_id))
        return "", 200
    except:
        return "", 404
    