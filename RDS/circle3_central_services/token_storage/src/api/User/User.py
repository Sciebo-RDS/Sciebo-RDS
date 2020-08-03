from flask import jsonify, request, abort
from werkzeug.exceptions import HTTPException
from RDS import User
import utility
import logging


def index():
    users = utility.storage.getUsers()
    data = {"list": users, "length": len(users)}
    return jsonify(data)


def get(user_id):
    try:
        return jsonify(utility.storage.getUser(user_id))
    except:
        abort(404, description=f"User {user_id} not found")


def post():
    user = None
    try:
        user = User.init(request.json)
    except:
        abort(400, description=f"Request not give a valid user object: {request.json}")

    utility.storage.addUser(user)

    data = {"success": True}
    return jsonify(data)


def delete(user_id):
    try:
        utility.storage.removeUser(utility.storage.getUser(user_id))
        data = {"success": True}
        return jsonify(data)
    except:
        abort(404, description="User not found")
