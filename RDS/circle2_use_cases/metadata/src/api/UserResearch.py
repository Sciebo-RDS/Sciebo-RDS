from lib.Metadata import Metadata
from flask import jsonify, current_app, request


def get(user_id, research_index):
    req = request.json

    md = Metadata(testing=current_app.config.get("TESTING"))
    
    researchId = md.getResearchId(
        userId=user_id, researchIndex=research_index)

    result = md.getMetadataForResearch(researchId=researchId, metadataFields=req)

    return jsonify({
        "researchId": researchId,
        "length": len(result),
        "list": result
    })
