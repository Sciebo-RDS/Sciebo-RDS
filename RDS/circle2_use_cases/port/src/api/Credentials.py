from flask import request
from RDS import Service, User, Token
import Util


def post():
    data = request.json

    user = User(data.get("username"))
    service = Util.tokenService.getService(data.get("servicename"), clean=True)
    token = Token(user, service, data.get("password"))

    return Util.tokenService.addTokenToUser(token)
