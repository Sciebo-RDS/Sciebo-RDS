import Singleton
from flask import jsonify, request
import logging

logger = logging.getLogger()


def get(user_id):
    result = []

    try:
        result = Singleton.ProjectService.getProject(user_id)
    except:
        return jsonify([]), 404

    return jsonify(result)


def post(user_id):
    result = None

<<<<<<< HEAD
    json = request.json
    try:
        portIn = json.get("portIn")
    except:
        portIn = []

    try:
        portOut = json.get("portOut")
    except:
        portOut = []

    result = Singleton.ProjectService.addProject(
        user_id, portIn=portIn, portOut=portOut)
=======
    try:
        json = request.json
        result = Singleton.ProjectService.addProject(
            user_id, portIn=json.get("portIn"), portOut=json.get("portOut"))
    except:
        result = Singleton.ProjectService.addProject(user_id)

>>>>>>> master
    return jsonify(result)
