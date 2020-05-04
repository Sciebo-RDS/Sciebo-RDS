from lib.Research import Research
from flask import jsonify


def index(user_id):
    pass


def get(user_id, research_id):
    return jsonify({"files": Research(userId=user_id, researchIndex=research_id)})


def post(user_id, research_id):
    return jsonify({"succ": Research(userId=user_id, researchIndex=research_id).synchronization()})


def delete(user_id, research_id):
    return jsonify({"succ": Research(userId=user_id, researchIndex=research_id).removeAllFiles()})
