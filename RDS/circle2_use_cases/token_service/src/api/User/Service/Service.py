import Util
from lib.Service import Service
from lib.User import User
from flask import jsonify


def get(user_id, servicename):
    return jsonify(Util.tokenService.getTokenForServiceFromUser(Service(servicename), User(user_id)))


def delete(user_id, servicename):
    return jsonify(Util.tokenService.removeTokenForServiceFromUser(
        Service(servicename), User(user_id)))
