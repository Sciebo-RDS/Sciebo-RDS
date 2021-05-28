import Util
from RDS import BaseService, User

from flask import jsonify, abort


def index(user_id, servicename):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))

    for svc in listOfServices:
        if svc.get("servicename", "") == servicename:
            return jsonify(svc.get("projects", []))
    abort(404)


def get(user_id, servicename, projects_id):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    projects_id = int(projects_id)
    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))

    for svc in listOfServices:
        projects = svc.get("projects", [])
        if svc.get("servicename", "") == servicename and projects_id < len(projects):
            return jsonify(projects[projects_id])

    abort(404)


def post(user_id, servicename):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    projectId, project = Util.tokenService.createProjectForUserInService(
        User(user_id), BaseService(servicename, implements=["metadata"]))
    return jsonify({"projectId": str(projectId)}), 204


def delete(user_id, servicename, projects_id):
    servicename = servicename.lower()
    if not servicename.startswith("port-"):
        servicename = "port-{}".format(servicename)

    if Util.tokenService.removeProjectForUserInService(
        User(user_id), BaseService(servicename,
                                   implements=["metadata"]), projects_id
    ):
        return None, 204
    abort(404)
