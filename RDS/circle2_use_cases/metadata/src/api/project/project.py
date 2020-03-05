from lib.Metadata import Metadata
from flask import jsonify, current_app, request


def get(project_id):
    result = Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id)

    return jsonify({"length": len(result), "list": result})


def patch(project_id):
    req = request.json
    mdService = Metadata(testing=current_app.config.get("TESTING"))
    result = mdService.updateMetadataForProject(project_id, req)

    return jsonify({"length": len(result), "list": result})
