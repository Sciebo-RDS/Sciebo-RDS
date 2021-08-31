import Singleton
from flask import jsonify, request, abort


def index(user_id, research_id):
    return jsonify({"researchname": Singleton.ProjectService.getProject(
        user_id, int(research_id)).researchname}
    )


def put(user_id, research_id):
    try:
        req = request.json
    except:
        return abort(400)

    name = req.get("researchname")

    project = Singleton.ProjectService.getProject(user_id, int(research_id))
    project.setResearchname(name)
    Singleton.ProjectService.setProject(user_id, project)
    return jsonify({"researchname": Singleton.ProjectService.getProject(
        user_id, int(research_id)).researchname}
    )
