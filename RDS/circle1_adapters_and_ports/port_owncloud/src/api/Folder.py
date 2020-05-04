from lib.ownCloudUser import OwncloudUser
from flask import request, send_file, jsonify
import logging
from connexion_plus import FlaskOptimize


logger = logging.getLogger()


@FlaskOptimize.do_not_minify()
@FlaskOptimize.do_not_compress()
def index():
    json = request.json
    userId = json.get("userId")
    apiKey = json.get("apiKey")
    filepath = json.get("filepath")
    logger.debug(f"userid {userId}")

    files = OwncloudUser(userId, apiKey).getFolder(filepath)

    return jsonify(files)
