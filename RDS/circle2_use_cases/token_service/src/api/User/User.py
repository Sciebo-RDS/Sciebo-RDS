import Util
from lib.User import User
from flask import jsonify


def get(user_id):
    return jsonify(Util.tokenService.getAllServicesForUser(User(user_id)))
