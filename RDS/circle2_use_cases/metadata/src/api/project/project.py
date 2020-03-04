from lib.Metadata import Metadata
from flask import jsonify, current_app


def get(project_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id))
