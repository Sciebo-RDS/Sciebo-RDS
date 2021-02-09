import Util
from RDS import BaseService, User
from flask import jsonify


def index(user_id):
    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))
    data = {"length": len(listOfServices), "list": listOfServices}

    return jsonify(data)


def get(user_id, servicename):
    servicename = servicename.lower()
    return jsonify(
        Util.tokenService.getTokenForServiceFromUser(
            BaseService(servicename.lower()), User(user_id)
        )
    )


def delete(user_id, servicename):
    servicename = servicename.lower()
    return jsonify(
        {
            "success": Util.tokenService.removeTokenForServiceFromUser(
                BaseService(servicename), User(user_id)
            )
        }
    )
