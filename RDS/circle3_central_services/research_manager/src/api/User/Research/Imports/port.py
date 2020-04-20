import Singleton
from flask import jsonify, request

import logging
logger = logging.getLogger()


def index(user_id, research_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortIn())


def post(user_id, research_id):
    json = request.json
    logger.debug(f"got json: {json}")
    from lib.Port import Port

    portname = json["port"]
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

    logger.debug(
        f"parsed data: port: {portname}, fs: {fs}, metadata: {md}, cp: {cp}")

    p = Port(portname, fileStorage=fs, metadata=md, customProperties=cp)

    Singleton.ProjectService.getProject(user_id, int(research_id)).addPortIn(p)
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortIn())


def get(user_id, research_id, port_id):
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortIn().get(int(port_id)))


def delete(user_id, research_id, port_id):
    Singleton.ProjectService.getProject(
        user_id, int(research_id)).removePortIn(int(port_id))
    return jsonify(Singleton.ProjectService.getProject(user_id, int(research_id)).getPortIn())
