from src.lib.Metadata import Metadata
from flask import jsonify, current_app


def index(project_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Identifiers", []))


def get(project_id, identifiers_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Identifiers", [])[identifiers_id])
