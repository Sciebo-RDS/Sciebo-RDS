from flask import request
from RDS import Service, User, Token
import Util


def post():
    data = request.json

    user = User(data.get("username"))
    service = Util.tokenService.getService(data.get("servicename"), clean=True)

    password = data.get("password")
    if password == "":
        password = "---"

    token = Token(user, service, password)

    return Util.tokenService.addTokenToUser(token)
