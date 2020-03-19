import Singleton
from flask import jsonify, request


def index(user_id, project_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(project_id)).getPortOut())


def post(user_id, project_id):
    json = request.json
    from lib.Port import Port

    fs = False
    md = False
    for prop in json.get("properties", []):
        if prop.get("portType", "") == "fileStorage":
            fs = prop["value"]
        elif prop.get("portType", "") == "metadata":
            md = prop["value"]

    p = Port(json["port"], fileStorage=fs, metadata=md)

    Singleton.ProjectService.getProject(user_id, int(project_id)).addPortOut(p)
    return jsonify(Singleton.ProjectService.getProject(user_id, int(project_id)).getPortOut())


def get(user_id, project_id, port_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(project_id)).getPortOut().get(int(port_id)))


def delete(user_id, project_id, port_id):
    Singleton.ProjectService.getProject(user_id, int(project_id)).removePortOut(int(port_id))
    return jsonify(Singleton.ProjectService.getProject(user_id, int(project_id)).getPortOut())
