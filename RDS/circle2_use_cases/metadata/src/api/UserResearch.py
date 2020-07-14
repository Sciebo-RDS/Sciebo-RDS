from lib.Metadata import Metadata
from flask import jsonify, current_app, request
import requests, os


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


def put(user_id, research_index):
    mdService = Metadata(testing=current_app.config.get("TESTING"))
    research_id = mdService.getResearchId(user_id, int(research_index))
    resp = mdService.publish(research_id)

    url = "{}".format(
        os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", current_app.config.get("TESTING"))
    )
    requests.put(
        "{}/research/user/{}/research/{}/status".format(url, user_id, research_index),
        verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
    )

    if resp:
        return None, 204

    return None, 400
