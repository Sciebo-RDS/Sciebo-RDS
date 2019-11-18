import logging
import os
from lib.upload_zenodo import Zenodo
from flask import jsonify, request

logger = logging.getLogger('')

z = Zenodo(os.getenv("ZENODO_API_KEY"))


def index(deposition_id):
    obj = z.get_deposition(deposition_id)
    creators = obj["metadata"]["creators"] if "creators" in obj["metadata"] else {}

    return jsonify(creators)


def get(deposition_id, creator_id):
    metadata = z.get_deposition(deposition_id)["metadata"]
    return metadata["creators"][creator_id]


def put(deposition_id, creator_id = -1):
    try:
        req_creators = request.json
        metadata = z.get_deposition(deposition_id)["metadata"]

        if creator_id > -1:
            creators_list = [] if not "creators" in metadata else metadata["creators"]
            creators_list.append(req_creators)

            metadata["creators"] = creators_list
        else:
            metadata["creators"] = req_creators

        ### the following have to be made, because zenodo wants this.
        if not "title" in metadata:
            metadata["title"] = "PLACEHOLDER"

        if not "description" in metadata:
            metadata["description"] = "PLACEHOLDER"

        if not "upload_type" in metadata:
            metadata["upload_type"] = "poster"
        ###

        logger.debug(f"Metadata: {metadata}")
        
        r = z.change_metadata_in_deposition(deposition_id=deposition_id, metadata=metadata, return_response=True)
        return True, r.status_code
    except Exception as e:
        logger.error(f"Error: \nDeposition-ID: {deposition_id}, creator-id: {creator_id} \nmessage: {e}")
        return False, 304


def delete(deposition_id, creator_id):
    metadata = z.get_deposition(deposition_id)["metadata"]
    creator_list = metadata["creators"]

    del creator_list[creator_id]
    metadata["creators"] = creator_list

    r = z.change_metadata_in_deposition(deposition_id, metadata)
    return r
