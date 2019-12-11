from flask import request, redirect


def index():
    code = None
    if "code" in request.args:
        code = request.args.get("code")

    state = None
    if "state" in request.args:
        state = request.args.get("state")

    if code is None or state is None:
        return redirect("/authorization_cancel")

    # TODO: generate an access_token for service and post it to C3-tokenStorage.
    # use state for servicename
    # use code as Authorization-code
    return redirect("/authorization_success")
