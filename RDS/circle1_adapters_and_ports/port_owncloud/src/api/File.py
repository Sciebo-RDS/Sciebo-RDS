from lib.ownCloudUser import OwncloudUser
from flask import request, send_file
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

    import os
    file = OwncloudUser(userId, apiKey).getFile(filepath)

    rv = send_file(file, attachment_filename=os.path.basename(
        filepath), as_attachment=False, mimetype="multipart/form-data")

    rv.direct_passthrough = False
    logger.debug("send response")
    return rv


@FlaskOptimize.do_not_minify()
@FlaskOptimize.do_not_compress()
def patch():
    raise NotImplementedError()


@FlaskOptimize.do_not_minify()
@FlaskOptimize.do_not_compress()
def post():
    raise NotImplementedError()


def delete():
    raise NotImplementedError()
