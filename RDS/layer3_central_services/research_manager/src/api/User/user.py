import Singleton
from flask import jsonify, request, abort
import logging
from time import time

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

    json = {}
    if request.is_json:
        json = request.get_json()
    
    portIn = json.get("portIn", [])
    portOut = json.get("portOut", [])
    
    result = Singleton.ProjectService.addProject(
        user_id, portIn=portIn, portOut=portOut, timeCreatedS=time()
    )
    return jsonify(result)


def delete(user_id):
    if Singleton.ProjectService.removeUser(user_id):
        return "", 204

    abort(404)
