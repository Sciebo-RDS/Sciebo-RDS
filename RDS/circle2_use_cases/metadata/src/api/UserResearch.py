from lib.Metadata import Metadata
from flask import jsonify, current_app


def get(user_id, research_index):
    researchId = Metadata(testing=current_app.config.get("TESTING")).getResearchId(
        userId=user_id, researchIndex=research_index)
    return jsonify({"researchId": researchId})
