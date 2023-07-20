from lib.Research import Research
from flask import jsonify, current_app
import json

def index(user_id):
    pass


def get(user_id, research_id):
    return jsonify(Research(userId=user_id, researchIndex=research_id, testing=current_app.config.get("TESTING")).getFiles())


def post(user_id, research_id):
    success, messages, results = Research(userId=user_id, researchIndex=research_id, testing=current_app.config.get("TESTING")).synchronization()
    return jsonify({
        "success" : success,
        "messages": json.loads(messages),
        "fileSuccess": json.loads(results)
    })


def delete(user_id, research_id):
    return jsonify({
        "succ": Research(userId=user_id, researchIndex=research_id, testing=current_app.config.get("TESTING")).removeAllFiles()
    })
