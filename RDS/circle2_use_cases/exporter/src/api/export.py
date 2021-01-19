from flask import request, current_app, jsonify
from lib.ExporterService import ExporterService
import logging

logger = logging.getLogger()

def post(toService):
    toService = toService.lower()
    json = request.values
    userId = json.get("user_id")
    fromService = json.get("from_service").lower()
    filepath = json.get("filename")

    logger.debug("userId: {}, fromService: {}, toService: {}, filepath: {}".format(userId, fromService, toService, filepath))

    result = ExporterService(testing=current_app.config.get("TESTING", False), testing_address=current_app.config.get(
        "TESTSERVER")).export(fromService, toService, filepath, userId)

    if result:
        return jsonify({"success": True})

    return "Export failed", 500
