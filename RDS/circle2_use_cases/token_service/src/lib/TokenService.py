import requests, os, json
from flask import jsonify

address = os.getenv("CENTRAL-SERVICE_TOKEN-STORAGE", "http://localhost:8081")

class TokenService():
    def __init__(self):
        pass

    def getOAuthURIForService(self, servicename):
        response = requests.get(f"{address}/service/{servicename}")
        # TODO check if servicename was valid
        data = json.loads(response.text)
        return data["authorize_url"]

    def getAllOAuthURIForService(self):
        response = requests.get(f"{address}/service")
        data = json.loads(response.text)

        return [svc["authorize_url"] for svc in data["list"]]
        
