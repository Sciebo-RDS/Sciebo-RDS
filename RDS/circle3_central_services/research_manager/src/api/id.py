import Singleton
from flask import jsonify

def get(research_id):
    result = Singleton.ProjectService.getProject(researchId=int(research_id))
    return jsonify(result)