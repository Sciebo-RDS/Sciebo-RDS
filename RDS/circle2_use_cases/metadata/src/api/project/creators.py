from src.lib.Metadata import Metadata
from flask import jsonify, current_app


def index(project_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Creators", []))


def get(project_id, creators_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Creators", [])[creators_id])


def post(project_id):
    pass


def patch(project_id, creators_id):
    pass
