import Singleton
from flask import jsonify, request


def get(user_id):
    try:
        return jsonify(Singleton.ProjectService.getProject(user_id))
    except:
        return jsonify([]), 404


def post(user_id):
    try:
        json = request.json
        return jsonify(Singleton.ProjectService.addProject(user_id, portIn=json.get("portIn"), portOut=json.get("portOut")))
    except:
        return jsonify(Singleton.ProjectService.addProject(user_id))
