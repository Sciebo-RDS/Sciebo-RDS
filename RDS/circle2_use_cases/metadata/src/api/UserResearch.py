from lib.Metadata import Metadata
from flask import jsonify, current_app


def get(user_id, research_index):
    md = Metadata(testing=current_app.config.get("TESTING"))
    
    researchId = md.getResearchId(
        userId=user_id, researchIndex=research_index)

    result = md.getMetadataForResearch(researchId=researchId)

    return jsonify({
        "researchId": researchId,
        "length": len(result),
        "list": result
    })
