from flask import jsonify
from RDS import FileTransferMode, LoginMode

def index():
    data = {
        "fileTransferArchive":False,
        "fileTransferMode":FileTransferMode.active,
        "loginMode":LoginMode.oauth
    }
    return jsonify(data)
