from lib.Metadata import Metadata
from lib.Research import Research
from flask import jsonify, current_app, request
import requests
import os
import json
from io import BytesIO
from RDS import Util


def get(user_id, research_index):
    req = request.json

    md = Metadata(testing=current_app.config.get("TESTING"))

    researchId = md.getResearchId(userId=user_id, researchIndex=research_index)

    result = md.getMetadataForResearch(
        researchId=researchId, metadataFields=req)

    return jsonify({"researchId": researchId, "length": len(result), "list": result})


def patch(user_id, research_index):
    try:
        req = request.json
    except:
        req = None

    if req is None or not req:
        # get ro crate file from portIn
        crates = []

        researchObj = Research(userId=user_id, researchIndex=research_index)
        for port in researchObj.portIn:
            filepath = ""

            for prop in port["properties"]:
                if prop["portType"] == "customProperties":
                    for cProp in prop["value"]:
                        if cProp["key"] == "filepath":
                            if str(cProp["value"]).endswith("/"):
                                filepath = "{}{}".format(
                                    cProp["value"], "ro-crate-metadata.json"
                                )
                            else:
                                filepath = "{}{}".format(
                                    cProp["value"], "/ro-crate-metadata.json"
                                )

            data = Util.parseToken(Util.loadToken(user_id, port["port"]))
            data["filepath"] = filepath

            crates.append(
                json.loads(
                    BytesIO(
                        requests.get(
                            "http://layer1-{}/storage/file".format(
                                port["port"]),
                            json=data,
                            verify=(os.environ.get(
                                "VERIFY_SSL", "True") == "True"),
                        ).content
                    )
                    .read()
                    .decode("UTF-8")
                )
            )

        # push ro crate content to all portOut metadata
        for crate in crates:
            for port in researchObj.portOut:
                projectId = ""

                for prop in port["properties"]:
                    if prop["portType"] == "customProperties":
                        for cProp in prop["value"]:
                            if cProp["key"] == "projectId":
                                projectId = cProp["value"]

                data = Util.parseToken(Util.loadToken(user_id, port["port"]))
                data["metadata"] = crate

                requests.patch(
                    "http://layer1-{}/metadata/project/{}".format(
                        port["port"], projectId
                    ),
                    json=data,
                    verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
                )

        return "", 202

    mdService = Metadata(testing=current_app.config.get("TESTING"))
    research_id = mdService.getResearchId(user_id, research_index)
    result = mdService.updateMetadataForResearch(research_id, req)

    return jsonify({"length": len(result), "list": result})


def put(user_id, research_index):
    mdService = Metadata(testing=current_app.config.get("TESTING"))
    research_id = mdService.getResearchId(user_id, int(research_index))
    resp = mdService.publish(research_id)

    url = "{}".format(
        os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER",
                  "{}/research".format(current_app.config.get("TESTING")))
    )
    requests.patch(
        "{}/user/{}/research/{}/status".format(
            url, user_id, research_index),
        verify=(os.environ.get("VERIFY_SSL", "True") == "True"), json={"finish": True}
    )

    if resp:
        return None, 204

    return None, 400
