from lib.Metadata import Metadata
from flask import jsonify, current_app, request


def get(user_id, research_index):
    req = request.json

    md = Metadata(testing=current_app.config.get("TESTING"))

    researchId = md.getResearchId(userId=user_id, researchIndex=research_index)

    result = md.getMetadataForResearch(researchId=researchId, metadataFields=req)

    return jsonify({"researchId": researchId, "length": len(result), "list": result})


def patch(user_id, research_index):
    req = request.json

    mdService = Metadata(testing=current_app.config.get("TESTING"))
    research_id = mdService.getResearchId(user_id, research_index)
    result = mdService.updateMetadataForResearch(research_id, req)

    return jsonify({"length": len(result), "list": result})
