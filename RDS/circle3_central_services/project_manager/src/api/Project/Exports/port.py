from Singleton import ProjectService
from flask import jsonify

def index(user_id, project_id):
    return jsonify(ProjectService.getProject(user_id, project_id).getPortOut())

def post(user_id, project_id):
    pass

def get(user_id, project_id, port_id):
    return jsonify(ProjectService.getProject(user_id, project_id).getPortOut().get(port_id))

def delete(user_id, project_id, port_id):
    pass