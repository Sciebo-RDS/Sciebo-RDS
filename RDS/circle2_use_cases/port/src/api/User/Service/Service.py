import Util
from RDS import BaseService, User
from flask import jsonify


def index(user_id):
    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))
    data = {"length": len(listOfServices), "list": listOfServices}

    return jsonify(data)


def get(user_id, servicename):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    return jsonify(
        Util.tokenService.getTokenForServiceFromUser(
            BaseService(servicename=servicename, implements=["metadata"]), User(user_id)
        )
    )


def delete(user_id, servicename):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    return jsonify(
        {
            "success": Util.tokenService.removeTokenForServiceFromUser(
                BaseService(servicename=servicename, implements=[
                            "metadata"]), User(user_id)
            )
        }
    )
