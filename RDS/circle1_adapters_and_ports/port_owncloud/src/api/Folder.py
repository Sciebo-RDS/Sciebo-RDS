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
        apiKey = Util.loadToken(json.get("userId"), "owncloud").access_token
    filepath = json.get("filepath")
    logger.debug(f"userid {userId}")

    files = OwncloudUser(userId, apiKey).getFolder(filepath)

    return jsonify({"files": files})
