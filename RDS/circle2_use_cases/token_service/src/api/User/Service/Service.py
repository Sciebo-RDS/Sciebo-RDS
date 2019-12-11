from lib.TokenService import TokenService
from lib.Service import Service
from lib.User import User
from flask import jsonify


def get(user_id, servicename):
    return jsonify(TokenService().getTokenForServiceFromUser(Service(servicename), User(user_id)))


def delete(user_id, servicename):
    return jsonify(TokenService().removeTokenForServiceFromUser(
        Service(servicename), User(user_id)))
