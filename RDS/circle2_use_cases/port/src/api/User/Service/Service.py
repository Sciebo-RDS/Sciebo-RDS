import Util
from lib.Service import Service
from lib.User import User
from flask import jsonify


def index(user_id):
    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))
    data = {
        "length": len(listOfServices),
        "list": listOfServices
    }

    return jsonify(data)


def get(user_id, servicename):
    return jsonify(Util.tokenService.getTokenForServiceFromUser(Service(servicename), User(user_id)))


def delete(user_id, servicename):
    return jsonify({"success": Util.tokenService.removeTokenForServiceFromUser(
        Service(servicename), User(user_id))})
