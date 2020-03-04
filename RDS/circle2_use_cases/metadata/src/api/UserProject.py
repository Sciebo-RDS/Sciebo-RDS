from src.lib.Metadata import Metadata
from flask import jsonify, current_app


def get(user_id, project_index):
    projectId = Metadata(testing=current_app.config.get("TESTING")).getProjectId(
        userId=user_id, projectIndex=project_index)
    return jsonify({"projectId": projectId})
