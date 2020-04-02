import Singleton
from flask import jsonify, request


def index(user_id, research_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortOut())


def post(user_id, research_id):
    json = request.json
    from lib.Port import Port

    fs = False
    md = False
    cp = None

    for prop in json.get("properties", []):
        if prop.get("portType", "") == "fileStorage":
            fs = prop["value"]
        elif prop.get("portType", "") == "metadata":
            md = prop["value"]
        elif prop.get("portType", "") == "customProperties":
            cp = prop["value"]

    p = Port(json["port"], fileStorage=fs, metadata=md, customProperties=cp)

    Singleton.ProjectService.getProject(user_id, int(research_id)).addPortOut(p)
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortOut())


def get(user_id, research_id, port_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortOut().get(int(port_id)))


def delete(user_id, research_id, port_id):
    Singleton.ProjectService.getProject(
        user_id, int(research_id)).removePortOut(int(port_id))
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortOut())
