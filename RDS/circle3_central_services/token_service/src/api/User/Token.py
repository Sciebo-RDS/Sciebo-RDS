from flask import jsonify, request
import Util
from lib.User import User

def index():
    return jsonify({})

def post(user_id):
    
    data = request.json
    try:
        mod = __import__('lib.Token', fromlist=data["type"])
        TokenType = getattr(mod, data["type"])
        print(TokenType)
    except:
        return "", 400
    
    Util.storage.addTokenToUser(User(user_id), TokenType(data["data"]))
    
    return "", 200
