import requests
import os

address = os.getenv("CENTRAL-SERVICE_TOKEN-STORAGE")

class TokenStorage():
    def __init__(self):
        pass

    def getOAuthURIForService(self, servicename):
        result = requests.get(f"{address}/service/{servicename}")
        return result.json()

    def getOAuthURIForServiceShort(self, servicename):
        result = requests.get(f"{address}/service/{servicename}/redirect_uri_full")
        return result.json()

