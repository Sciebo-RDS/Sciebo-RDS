from lib.TokenService import TokenService
from lib.Service import Service
from lib.User import User


def get(user_id, servicename):
    TokenService().getTokenForServiceFromUser(Service(servicename), User(user_id))


def delete(user_id, servicename):
    TokenService().removeTokenForServiceFromUser(
        Service(servicename), User(user_id))
