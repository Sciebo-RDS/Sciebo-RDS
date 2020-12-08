from flask import jsonify
from RDS import FileTransferMode, LoginMode

def index():
    data = {
        "fileTransferArchive":"",
        "fileTransferMode":FileTransferMode.active.value,
        "loginMode":LoginMode.oauth.value
    }
    return jsonify(data)
