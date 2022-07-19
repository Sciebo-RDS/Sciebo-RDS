from lib.ownCloudUser import OwncloudUser
from flask import request, send_file, jsonify
import logging
from connexion_plus import FlaskOptimize
from RDS import Util


logger = logging.getLogger()


@FlaskOptimize.do_not_minify()
@FlaskOptimize.do_not_compress()
def index():
    json = request.json
    try:
        service, userId, apiKey = Util.parseUserId(json.get("userId"))
    except:
        apiKey = Util.loadToken(json.get("userId"), "port-owncloud").access_token
    filepath = json.get("filepath")
    logger.debug(f"userid {userId}")

    files = OwncloudUser(userId, apiKey).getFolder(filepath)

    return jsonify({"files": files})


@FlaskOptimize.do_not_minify()
@FlaskOptimize.do_not_compress()
def post():
    json = request.json

    try:
        _, userId, apiKey = Util.parseUserId(json.get("userId"))
    except:
        apiKey = Util.loadToken(json.get("userId"), "port-owncloud").access_token
    filepath = json.get("filepath")
    logger.debug(f"userid {userId}")

    link = OwncloudUser(userId, apiKey).createSharelink(filepath)

    return jsonify({"sharelink": link})
