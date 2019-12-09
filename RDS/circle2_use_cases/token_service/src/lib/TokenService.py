import requests, os, json
from flask import jsonify


class TokenService():
    def __init__(self):
        self.address = os.getenv("CENTRAL-SERVICE_TOKEN-STORAGE", "http://localhost:8081")

    def getOAuthURIForService(self, servicename):
        response = requests.get(f"{self.address}/service/{servicename}")
        
        if response.status_code == 404:
            raise ServiceNotFoundError(servicename)

        data = json.loads(response.text)
        return data["authorize_url"]

    def getAllOAuthURIForService(self):
        response = requests.get(f"{self.address}/service")
        data = json.loads(response.text)

        return [svc["authorize_url"] for svc in data["list"]]
        
