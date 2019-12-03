from flask import jsonify, request
import json, Util
from lib.User import User
from lib.Exceptions.StorageException import UserHasTokenAlreadyError

def index(user_id):
    data = Util.storage.getToken(user_id)
    return jsonify(data)

def post(user_id):
    TokenType = Util.load_class_from_json(request.json)
    Util.storage.addTokenToUser(TokenType.from_json(request.json), User(user_id))
    
    return "", 200

def get(user_id, token_id):
    token = Util.storage.getToken(user_id, int(token_id))
    return jsonify(token)

def delete(user_id, token_id):
    user = Util.storage.getUser(user_id)
    token = Util.storage.getToken(user_id, int(token_id))

    Util.storage.removeToken(user, token)
    return "", 200
