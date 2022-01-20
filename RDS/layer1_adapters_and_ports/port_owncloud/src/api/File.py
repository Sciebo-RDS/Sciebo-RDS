from lib.ownCloudUser import OwncloudUser, parseCloudId
from flask import request, send_file
import logging
from connexion_plus import FlaskOptimize
from RDS import Util
import json
import os

logger = logging.getLogger()

# FIXME: Maybe this could be a problem with fork via gunicorn
webdavFilePath = os.getenv("WEBDAVSERVER_FILE", "webdav.json")
lookupWebdav = None

if os.path.isfile(webdavFilePath):
    with open(webdavFilePath, "r") as webdavFile:
        lookupWebdav = json.load(open(webdavFile))


@FlaskOptimize.do_not_minify()
@FlaskOptimize.do_not_compress()
def index():
    jsonData = request.json
    try:
        service, userId, apiKey = Util.parseUserId(jsonData.get("userId"))
    except:
        userId = jsonData.get("userId")
        service = "port-owncloud"
        apiKey = Util.loadToken(userId, service).access_token

    filepath = jsonData.get("filepath")
    logger.debug(f"userid {userId} for service {service}")

    webdavServer = None

    if lookupWebdav is not None:
        userId, server = parseCloudId(userId)
        webdavServer = lookupWebdav[server]["webdav"]

    file = OwncloudUser(userId, apiKey, webdavServer).getFile(filepath)

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
