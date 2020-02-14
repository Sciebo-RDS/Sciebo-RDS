from flask import request, current_app, jsonify
from lib.ExporterService import ExporterService
import logging

logger = logging.getLogger()

def post(toService):
    json = request.get_json(force=True)
    userId = json.get("user_id")
    fromService = json.get("from_service")
    filepath = json.get("filename")

    result = ExporterService(testing=current_app.config.get("TESTING", False), testing_address=current_app.config.get(
        "TESTSERVER")).export(fromService, toService, filepath, userId)

    if result:
        return jsonify({"success": True})

    return "Export failed", 500
