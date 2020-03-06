import Singleton
from flask import jsonify

def get(project_id):
    result = Singleton.ProjectService.getProject(identifier=int(project_id))
    return jsonify(result)