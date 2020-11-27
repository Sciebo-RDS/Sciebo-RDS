from flask import jsonify
from RDS import FileTransferMode, LoginMode

def index():
    data = {
        "fileTransferArchive":"zip",
        "fileTransferMode":FileTransferMode.active,
        "loginMode":LoginMode.oauth
    }
    return jsonify(data)
