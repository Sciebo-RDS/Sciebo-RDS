from lib.ownCloudUser import OwncloudUser
from flask import request, send_file
import logging

logger = logging.getLogger()


def get(filepath):
    userId = request.values.get("userId")
    logger.debug(f"userid {userId}")

    rv = send_file(OwncloudUser(userId).getFile(filepath), attachment_filename=filepath,
                   conditional=True, as_attachment=True, mimetype="application/octet-stream")
    logger.debug("disable passthrough")
    rv.direct_passthrough = False
    return rv
