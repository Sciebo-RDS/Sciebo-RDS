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
            {"projectId": str(depo.id), "metadata": depo.metadata(jsonld=True)}
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
        try:
            project = g.osf.create_project_jsonld(req)

        except:
            project = g.osf.create_project(
                req["title"],
                req.get("osf_category", "project"),
                description=req.get("description", ""),
                tags=req.get("tags", ""),
            )

        return jsonify(
            {"projectId": project.id, "metadata": project.metadata(jsonld=True)}
        )
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

    if project.update(req):
        return jsonify(project.metadata(jsonld=True))

    abort(500)


@require_api_key
def put(project_id):
    project = g.osf.project(project_id)
    project.public = True

    if project.update():
        return True, 200

    abort(400)
