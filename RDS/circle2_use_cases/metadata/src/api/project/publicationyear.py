from src.lib.Metadata import Metadata
from flask import jsonify, current_app


def index(project_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("PublicationYear", []))


def patch(project_id):
    pass
