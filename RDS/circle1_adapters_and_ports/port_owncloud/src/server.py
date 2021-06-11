#!/usr/bin/env python

from RDS import Util, OAuth2Service, FileTransferMode, FileTransferArchive
from __init__ import app
from RDS import Util
import os

owncloud_installation_url = os.getenv("OWNCLOUD_INSTALLATION_URL", "")
owncloud_redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
owncloud_oauth_token_url = "{}/index.php/apps/oauth2/api/v1/token".format(
    owncloud_installation_url
)
owncloud_oauth_id = os.getenv("OWNCLOUD_OAUTH_CLIENT_ID", "XY")
owncloud_oauth_secret = os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET", "ABC")

owncloud_oauth_authorize = "{}/index.php/apps/oauth2/authorize%3Fredirect_uri={}&response_type=code&client_id={}".format(
    owncloud_installation_url, owncloud_redirect_uri, owncloud_oauth_id
)

service = OAuth2Service(
    servicename="port-owncloud",
    implements=["fileStorage"],
    fileTransferMode=FileTransferMode.active,
    fileTransferArchive=FileTransferArchive.none,
    authorize_url=owncloud_oauth_authorize,
    refresh_url=owncloud_oauth_token_url,
    client_id=owncloud_oauth_id,
    client_secret=owncloud_oauth_secret,
    description={"en": "ownCloud is a suite of client–server software for creating and using file hosting services.",
                 "de": "ownCloud ist eine Suite von Client-Server-Software zur Erstellung und Nutzung von File-Hosting-Diensten."},
    displayName="ownCloud",
    infoUrl="https://owncloud.com/",
    helpUrl="https://owncloud.com/docs-guides/",
    icon="./owncloud.svg"
)
Util.register_service(service)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server="gevent")
