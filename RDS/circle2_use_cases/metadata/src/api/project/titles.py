from lib.Metadata import Metadata
from flask import jsonify, current_app


def index(project_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Titles", []))


def get(project_id, title_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Identifiers", [])[title_id])


def post(project_id):
    pass


def patch(project_id, title_id):
    pass
