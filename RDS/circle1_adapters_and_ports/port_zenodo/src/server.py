#!/usr/bin/env python

from RDS import Util, OAuth2Service, FileTransferMode, FileTransferArchive
from __init__ import app, register_service
import os


redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
zenodo_address = os.getenv("ZENODO_ADDRESS", "https://sandbox.zenodo.org")
zenodo_oauth_token_url = "{}/oauth/token".format(zenodo_address)
zenodo_oauth_id = os.getenv("ZENODO_OAUTH_CLIENT_ID", "XY")
zenodo_oauth_secret = os.getenv("ZENODO_OAUTH_CLIENT_SECRET", "ABC")

zenodo_oauth_authorize = "{}/oauth/authorize%3Fredirect_uri={}&response_type=code&scope%3Ddeposit%3Awrite%20deposit%3Aactions&client_id={}".format(
    zenodo_address, redirect_uri, zenodo_oauth_id
)

service = OAuth2Service(
    servicename="port-zenodo",
    implements=["metadata"],
    fileTransferMode=FileTransferMode.active,
    fileTransferArchive=FileTransferArchive.zip,
    authorize_url=zenodo_oauth_authorize,
    refresh_url=zenodo_oauth_token_url,
    client_id=zenodo_oauth_id,
    client_secret=zenodo_oauth_secret,
    description="Zenodo is a general-purpose open-access repository developed under the European OpenAIRE program and operated by CERN. It allows researchers to deposit data sets, research software, reports, and any other research related digital artifacts."
)
Util.register_service(service)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server='gevent')
