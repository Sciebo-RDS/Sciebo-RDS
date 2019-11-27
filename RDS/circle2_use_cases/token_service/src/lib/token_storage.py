import requests, os, json
from flask import jsonify

address = os.getenv("CENTRAL-SERVICE_TOKEN-STORAGE")

class TokenStorage():
    def __init__(self):
        pass

    def getOAuthURIForService(self, servicename):
        response = requests.get(f"{address}/service/{servicename}")
        return response.text

    def getOAuthURIForServiceShort(self, servicename):
        response = self.getOAuthURIForService(servicename)
        data = json.loads(response)
        return data["redirect_uri_full"]

