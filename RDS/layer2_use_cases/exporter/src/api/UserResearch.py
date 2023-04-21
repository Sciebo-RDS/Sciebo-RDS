from lib.Research import Research
from flask import jsonify, current_app

def index(user_id):
    pass


def get(user_id, research_id):
    return jsonify(Research(userId=user_id, researchIndex=research_id, testing=current_app.config.get("TESTING")).getFiles())


def post(user_id, research_id):
    result = Research(userId=user_id, researchIndex=research_id, testing=current_app.config.get("TESTING")).synchronization()
    return jsonify({
        "success" : result[0],
        "messages": result[1]
    })


def delete(user_id, research_id):
    return jsonify({
        "succ": Research(userId=user_id, researchIndex=research_id, testing=current_app.config.get("TESTING")).removeAllFiles()
    })
