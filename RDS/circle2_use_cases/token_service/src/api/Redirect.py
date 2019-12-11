from flask import request, redirect
from lib.TokenService import TokenService
import jwt
import os
import requests
from jwt.exceptions import InvalidSignatureError
import Util

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)


def index():
    code = None
    if "code" in request.args:
        code = request.args.get("code")

    state = None
    if "state" in request.args:
        state = request.args.get("state")

    if code is None or state is None:
        return redirect("/authorization_cancel")

    # use state for servicename
    data = None
    try:
        data = jwt.decode(state, TokenService().secret, algorithms="HS256")
    except InvalidSignatureError:
        return redirect("/authorization_cancel")

    # get service from tokenStorage for whom the code is
    response = requests.get(f"{address}/service/{data["servicename"]}")

    if response.status_code is not 200:
        return redirect("/authorization_cancel")

    service = load_object(response.text)

    # FIXME: FLASK_HOST_ADDRESS needs to be set in dockerfile
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{os.getenv("FLASK_HOST_ADDRESS", "http://localhost:8080")}/redirect"
    }

    response = requests.post(f"{service.refresh_url}", data=body, auth=(
        service.client_id, service.client_secret))

    if response.status_code is not 200:
        return redirect("/authorization_cancel")

    access_token_from_service = response.json()

    # save the access_token in tokenStorage
    response = requests.post(f"{address}/{access_token_from_service["user_id"]}/token", data=access_token_from_service)

    if response.status_code is not 200:
        return redirect("/authorization_cancel")

    return redirect("/authorization_success")
