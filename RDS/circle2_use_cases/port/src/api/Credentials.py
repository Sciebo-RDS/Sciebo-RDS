from flask import request
from RDS import Service, User, LoginToken
import Util


def post():
    data = request.json

    rootUser = User(data.get("userId"))
    service = Util.tokenService.getService(data.get("servicename").lower(), clean=True)
    token = LoginToken(User(data.get("username")), service, data.get("password"))

    return Util.tokenService.addTokenToUser(token, rootUser)
