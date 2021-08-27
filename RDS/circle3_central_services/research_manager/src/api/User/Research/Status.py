import Singleton
from flask import jsonify


def index(user_id, research_id):
    result = Singleton.ProjectService.getProject(
        user_id, int(research_id)).status
    return jsonify({"status": result})


def patch(user_id, research_id):
    Singleton.ProjectService.bumpProject(user_id, int(research_id))

    result = Singleton.ProjectService.getProject(
        user_id, int(research_id)).status
    return jsonify({"status": result})
