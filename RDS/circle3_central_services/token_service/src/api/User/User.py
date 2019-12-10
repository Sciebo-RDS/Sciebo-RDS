from flask import jsonify, request, abort
from werkzeug.exceptions import HTTPException
import Util
from lib.User import User
import logging


def index():
    users = Util.storage.getUsers()
    data = {
        "list": users,
        "length": len(users)
    }
    return jsonify(data)


def get(user_id):
    try:
        return jsonify(Util.storage.getUser(user_id))
    except:
        abort(404, description=f"User {user_id} not found")


def post():
    user = None
    try:
        req = request.json
        user = User(req["username"])
    except:
        abort(400, description=f"Request not give a valid user object: {request.json}")
    
    Util.storage.addUser(user)

    data = {
        "success": True
    }
    return jsonify(data)


def delete(user_id):
    try:
        Util.storage.removeUser(User(user_id))
        data = {
            "success": True
        }
        return jsonify(data)
    except:
        abort(404, description="User not found")
