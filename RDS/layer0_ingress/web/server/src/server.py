from flask_cors import CORS
from flask import Response, stream_with_context, session, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    UserMixin,
    login_required,
    logout_user,
    current_user,
)
from .app import app, socketio, user_store, use_predefined_user, use_embed_mode, use_proxy, redirect_url
from .websocket import exchangeCodeData, RDSNamespace
import json
import requests
import uuid
import os
import os
import jwt

CORS(app, origins=json.loads(os.getenv("FLASK_ORIGINS")), supports_credentials=True)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
socketio.on_namespace(RDSNamespace("/"))

req = requests.get(
    "{}/apps/rds/api/1.0/publickey".format(
        os.getenv("OWNCLOUD_URL",
                  "https://10.14.29.60/owncloud/index.php")
    ),
    verify=os.getenv("VERIFY_SSL", "False") == "True"
).json()

publickey = req.get("publickey", "").replace("\\n", "\n")


def proxy(host, path):
    req = requests.get(f"{host}{path}", stream=True, timeout=1)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)), content_type=req.headers['content-type'])


class User(UserMixin):

    def to_dict(self):
        return {
            "id": self.id,
            "websocketId": self.websocketId,
            "userId": self.userId,
            "token": self.token
        }

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)

    def __init__(self, id=None, userId=None, websocketId=None, token=None):
        super().__init__()
        if id is None:
            raise ValueError("id needs to be set-")

        self.id = id
        self.websocketId = websocketId
        self.userId = userId
        self.token = token

        if userId is None:
            headers = {
                "Authorization": f"Bearer {token}"
            }

            req = requests.get(
                "{}/apps/rds/api/1.0/informations".format(
                    os.getenv("OWNCLOUD_URL",
                              "https://10.14.29.60/owncloud/index.php")
                ),
                headers=headers,
                verify=os.getenv("VERIFY_SSL", "False") == "True",
            )

            if req.status_code == 200:
                text = req.json()["jwt"]

                data = jwt.decode(
                    text, publickey, algorithms=["RS256"]
                )
                app.logger.debug(data)

                self.userId = data["name"]
                return
            raise ValueError


@app.route("/informations")
def informations():
    data = {}

    if redirect_url is not None:
        data["redirectUrl"] = redirect_url

    return json.dumps(data)


@app.route("/faq")
def questions():
    from .questions import questions

    return json.dumps(questions)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ("", 200) if (current_user.is_authenticated) else ("", 401)

    try:
        reqData = request.get_json()
    except Exception as e:
        app.logger.error(e, exc_info=True)
        reqData = request.form
    app.logger.debug("reqdata: {}".format(reqData))

    user = None
    if publickey != "":
        try:
            decoded = jwt.decode(
                reqData.get("informations", ""), publickey, algorithms=["RS256"]
            )

            user = User(
                id=str(uuid.uuid4()),
                userId=decoded["name"]
            )

            session["informations"] = decoded
        except Exception as e:
            app.logger.error(e, exc_info=True)

    if user is not None:
        user_store[user.get_id()] = user.to_dict()
        login_user(user)
        app.logger.info("logged? {}".format(current_user.is_authenticated))

        return "", 201

    return "", 401


@login_manager.user_loader
def load_user(user_id):
    return User.from_dict(user_store.get(user_id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def index(path):
    if use_embed_mode and use_predefined_user:
        app.logger.debug("skip authentication")
        user = User(
            id=str(uuid.uuid4()), userId=os.getenv("DEV_FLASK_USERID")
        )
        user_store[user.get_id()] = user.to_dict()
        login_user(user)

    if "access_token" in request.args:
        user = User(
            id=str(uuid.uuid4()),
            token=request.args["access_token"]
        )
        user_store[user.get_id()] = user.to_dict()
        login_user(user)
        return redirect("/")

    if current_user.is_authenticated:
        if "code" in request.args and "state" in request.args:
            if exchangeCodeData(request.args):
                return app.send_static_file("exchangeCode.html")
            return app.send_static_file("exchangeCode_error.html")

    if use_embed_mode or current_user.is_authenticated:
        if use_proxy:
            return proxy(os.getenv("DEV_WEBPACK_DEV_SERVER_HOST"), request.path)

    if use_embed_mode:
        return app.send_static_file(path)

    return redirect(
        redirect_url
    )
