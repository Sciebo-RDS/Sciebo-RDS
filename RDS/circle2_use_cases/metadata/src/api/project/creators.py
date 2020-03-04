from lib.Metadata import Metadata
from flask import jsonify, current_app


def index(project_id):
    metadataPortList = Metadata(testing=current_app.config.get(
        "TESTING")).getMetadataForProject(projectId=project_id)
    result = []

    for metadata in metadataPortList:
        port = metadata["port"]
        md = metadata["metadata"]

        result.append({
            "port": port,
            "metadata": md
        })

    return jsonify({"list": result, "length": len(result)})


def get(project_id, creators_id):
    return jsonify(Metadata(testing=current_app.config.get("TESTING")).getMetadataForProject(projectId=project_id).get("Creators", [])[creators_id])


def post(project_id):
    pass


def patch(project_id, creators_id):
    pass
