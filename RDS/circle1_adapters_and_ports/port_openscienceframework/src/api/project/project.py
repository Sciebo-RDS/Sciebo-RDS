import logging
import os
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort
from lib.Util import require_api_key

logger = logging.getLogger()


@require_api_key
def index():
    req = request.json.get("metadata")

    depoResponse = g.osf.projects()
    return jsonify(
        [
            {"projectId": str(depo.id), "metadata": depo.metadata()}
            for depo in depoResponse
        ]
    )


@require_api_key
def get(project_id):
    req = request.json.get("metadata")

    depoResponse = g.osf.project(project_id)

    return jsonify(depoResponse)


@require_api_key
def post():
    req = request.json.get("metadata")

    try:
        project = g.osf.create_project(
            title=req["title"],
            category=req["osf_category"],
            description=req["description"],
            tags="",
        )

        return jsonify({"projectId": project.id, "metadata": project.metadata(),})
    except:
        abort(500)


@require_api_key
def delete(project_id):
    if g.osf.project(project_id).delete():
        return "", 204

    abort(404)


@require_api_key
def patch(project_id):
    req = request.get_json(force=True, cache=True).get("metadata")

    project = g.osf.project(project_id)

    for key, value in req.items():
        setattr(project, key, value)

    if project.update():
        return jsonify(project.metadata())

    abort(500)


@require_api_key
def put(project_id):
    project = g.osf.project(project_id)
    project.public = True

    if project.update():
        return True, 200

    abort(400)
