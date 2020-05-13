import Util
from lib.Service import Service
from lib.User import User

from flask import jsonify, abort


def index(user_id, servicename):
    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))

    for svc in listOfServices:
        if svc.servicename == servicename:
            return jsonify(svc)
    abort(404)


def get(user_id, servicename, projects_id):
    listOfServices = Util.tokenService.getAllServicesForUser(User(user_id))

    for svc in listOfServices:
        if svc.get(servicename, "") == servicename and projects_id < len(svc.projects):
            return jsonify(svc.projects[projects_id])
    abort(404)


def post(user_id, servicename):
    Util.tokenService.createProjectForUserInService(
        User(user_id), Service(servicename))
    return None, 204


def delete(user_id, servicename, projects_id):
    if Util.tokenService.removeProjectForUserInService(User(user_id), Service(servicename), projects_id):
        return None, 204
    abort(404)
