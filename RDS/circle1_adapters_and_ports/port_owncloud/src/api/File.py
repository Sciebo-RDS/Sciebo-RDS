from lib.ownCloudUser import OwncloudUser
from flask import request, send_file
import logging

logger = logging.getLogger()


def get(filepath):
    userId = request.values["userId"]
    logger.debug(f"userid {userId}")

    rv = send_file(OwncloudUser(userId).getFile(filepath), attachment_filename=filepath, conditional=True)
    logger.debug("disable passthrough")
    rv.direct_passthrough = False
    return rv
