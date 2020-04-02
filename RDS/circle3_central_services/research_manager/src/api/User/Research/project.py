import Singleton
from flask import jsonify


def get(user_id, research_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)))


def delete(user_id, research_id):
    resp = Singleton.ProjectService.removeProject(user_id, int(research_id))

    if resp:
        return None, 204

    raise Exception(f"given project with id {research_id} not removed")

