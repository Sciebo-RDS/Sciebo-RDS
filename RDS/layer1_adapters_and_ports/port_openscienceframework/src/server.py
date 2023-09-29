#!/usr/bin/env python

from RDS import Util, OAuth2Service, FileTransferMode, FileTransferArchive
from __init__ import app
import os


redirect_uri = os.getenv("RDS_OAUTH_REDIRECT_URI", "")
osf_address = os.getenv("OPENSCIENCEFRAMEWORK_ADDRESS",
                        "https://accounts.test.osf.io")
osf_oauth_token_url = "{}/oauth2/token".format(osf_address)
osf_oauth_id = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_ID", "XY")
osf_oauth_secret = os.getenv("OPENSCIENCEFRAMEWORK_OAUTH_CLIENT_SECRET", "ABC")


osf_oauth_authorize = "{}/oauth2/authorize?response_type=code&redirect_uri={}&client_id={}&scope=osf.full_write&access_type={}".format(
    osf_address, redirect_uri, osf_oauth_id, "offline"
)
osf_display_name = os.getenv("OPENSCIENCEFRAMEWORK_DISPLAYNAME", "OpenScienceFramework")
osf_info_url = os.getenv("OPENSCIENCEFRAMEWORK_INFO_URL","https://osf.io/")
osf_help_url = os.getenv("OPENSCIENCEFRAMEWORK_HELP_URL","https://help.osf.io/hc/en-us")
osf_icon = os.getenv("OPENSCIENCEFRAMEWORK_ICON","./osf.png")
osf_metadata_profile = os.getenv("OPENSCIENCEFRAMEWORK_METADATA_PROFILE","./metadata_profile.json")
osf_project_link_template = os.getenv("OPENSCIENCEFRAMEWORK_PROJECT_LINK_TEMPLATE","https://osf.io/${projectId}")


service = OAuth2Service(
    servicename="port-openscienceframework",
    implements=["metadata"],
    fileTransferMode=FileTransferMode.active,
    fileTransferArchive=FileTransferArchive.none,
    authorize_url=osf_oauth_authorize,
    refresh_url=osf_oauth_token_url,
    client_id=osf_oauth_id,
    client_secret=osf_oauth_secret,
    description={"en": "OSF is a free, open platform to support your research and enable collaboration. It helps you and your colleagues to manage your project throughout its entire lifecycle.",
                 "de": "OSF ist eine kostenlose, offene Plattform, die Ihre Forschung unterstützt und Zusammenarbeit ermöglicht. Es hilft Ihnen und Ihren Kollegen, Ihr Projekt während seines gesamten Lebenszyklus zu verwalten."},
    displayName=osf_display_name,
    infoUrl=osf_info_url,
    helpUrl=osf_help_url,
    icon=osf_icon,
    metadataProfile=osf_metadata_profile,
    projectLinkTemplate=osf_project_link_template
)

Util.register_service(service)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server="gevent")
