import Singleton
from flask import jsonify


def index(user_id, project_id):
    result = Singleton.ProjectService.getProject(
        user_id, int(project_id)).status
    return jsonify({"status": result})


def patch(user_id, project_id):
    result = Singleton.ProjectService.getProject(
        user_id, int(project_id)).nextStatus()
    return jsonify({"status": result})
