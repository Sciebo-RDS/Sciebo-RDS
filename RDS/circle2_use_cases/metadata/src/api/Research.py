from lib.Metadata import Metadata
from flask import jsonify, current_app, request


def get(research_id):
    req = request.json

    result = Metadata(testing=current_app.config.get("TESTING")).getMetadataForResearch(researchId=research_id, metadataFields=req)

    return jsonify({"length": len(result), "list": result})


def patch(research_id):
    req = request.json
    
    mdService = Metadata(testing=current_app.config.get("TESTING"))
    result = mdService.updateMetadataForResearch(research_id, req)

    return jsonify({"length": len(result), "list": result})
