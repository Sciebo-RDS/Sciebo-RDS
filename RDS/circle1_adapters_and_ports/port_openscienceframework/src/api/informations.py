from flask import jsonify
from RDS import FileTransferMode, LoginMode

def index():
    data = {
        "fileTransferArchive":"zip",
        "fileTransferMode":FileTransferMode.active.value,
        "loginMode":LoginMode.oauth.value
    }
    return jsonify(data)
