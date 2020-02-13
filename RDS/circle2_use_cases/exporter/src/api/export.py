from flask import request, current_app
from lib.ExporterService import ExporterService
import logging

logger = logging.getLogger()

def post(toService):
    json = request.json
    userId = json.get("user_id")
    fromService = json.get("from_service")
    filepath = json.get("filename")

    result = ExporterService(testing=current_app.config.get("TESTING", False), testing_address=current_app.config.get(
        "TESTSERVER", None)).export(fromService, toService, filepath, userId)

    if result:
        return True

    return "Export failed", 500
