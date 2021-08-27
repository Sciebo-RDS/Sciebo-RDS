import Singleton
from flask import jsonify, request


def index(user_id, research_id):
    result = Singleton.ProjectService.getProject(
        user_id, int(research_id)).status
    return jsonify({"status": result})


def patch(user_id, research_id):
    try:
        req = request.json
    except:
        req = None

    if req is not None and req.get("finish") == True:
        Singleton.ProjectService.finishProject(user_id, int(research_id))
    else:
        Singleton.ProjectService.bumpProject(user_id, int(research_id))

    result = Singleton.ProjectService.getProject(
        user_id, int(research_id)).status
    return jsonify({"status": result})
