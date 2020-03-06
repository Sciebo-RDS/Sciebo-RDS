import Singleton
from flask import jsonify

def get(project_id):
    result = Singleton.ProjectService.getProject(projectId=int(project_id))
    return jsonify(result)