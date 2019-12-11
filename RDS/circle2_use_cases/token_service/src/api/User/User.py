from lib.TokenService import TokenService
from lib.User import User
from flask import jsonify


def get(user_id):
    return jsonify(TokenService().getAllServicesForUser(User(user_id)))
