import logging

logger = logging.getLogger('')

def search(deposition_id):
    pass

def get(deposition_id, creator_id = -1):
    if creator_id >= 0:
        return "creator {}".format(creator_id)
    return "Testitest"

def index(deposition_id):
    obj = z.get_deposition(deposition_id)
    creators = obj["metadata"]["creators"] if "creators" in obj["metadata"] else {}

    return jsonify(creators)
def put(deposition_id, creator_id = -1):
    pass

def delete(deposition_id, creator_id = -1):
    pass
