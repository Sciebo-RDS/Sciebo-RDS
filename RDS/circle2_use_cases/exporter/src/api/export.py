from flask import request
from lib.ExporterService import ExporterService

def post(toService):
    userId = request.values.get("user_id")
    fromService = request.values.get("from_service")
    filepath = request.values.get("filename")

    result = ExporterService().export(fromService, toService, filepath, userId)

    if result:
        return True
        
    return "Export failed", 500