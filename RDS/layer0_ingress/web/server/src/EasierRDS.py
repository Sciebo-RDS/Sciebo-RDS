import logging
import requests
import os
import json
import re
from flask_login import current_user
from .app import use_predefined_user, app, use_tests_folder


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def parseDict(data, socketio=None, httpManager=None):
    if (socketio or httpManager) is None:
        raise ValueError("socketio and httpManager are none.")

    httpManager = httpManager or HTTPManager(socketio=socketio)

    for key, value in data.items():
        http = HTTPRequest(key)

        for val in value:
            http.addRequest(*val)

        httpManager.addService(http)

    return httpManager


class HTTPRequest:
    def __init__(self, url):
        self.url = url
        self.requestList = {}

    def addRequest(self, key, url, method="get", beforeFunction=None, afterFunction=None, clear=False):
        """This method adds a request to sciebo RDS.

        Args:
            key ([type]): [description]
            url ([type]): [description]
            method (str, optional): [description]. Defaults to "get".
            beforeFunction ([type], optional): [description]. Defaults to None.
            afterFunction ([type], optional): [description]. Defaults to None.
            clear (bool, optional): True, if the functions should get the response object itself, instead of already json unserialized object. Defaults to False.
        """
        self.requestList[key] = {
            "url": url,
            "method": method,
            "before": beforeFunction,
            "after": afterFunction,
            "giveResponseObject": clear
        }

    def makeRequest(self, key, data=None):
        if data is None:
            data = {}

        if isinstance(data, str):
            data = json.loads(data)

        reqConf = self.requestList[key]

        if reqConf["before"] is not None:
            try:
                data = reqConf["before"](data)
            except:
                pass

        if use_predefined_user:
            data["userId"] = os.getenv("DEV_FLASK_USERID")
        else:
            data["userId"] = current_user.userId

        data["url"] = self.url

        app.logger.debug(
            "key: {}, data: {}, req: {}".format(key, data, reqConf))

        sendEmptyData = False

        group = re.findall(r"{\w*}", reqConf["url"])
        app.logger.debug("url: {}, found groups: {}, len groups: {}, len data: {}, equal: {}".format(
            reqConf["url"], group, len(group), len(
                data), len(group) == len(data)
        ))
        if len(group) == len(data):
            sendEmptyData = True

        url = reqConf["url"].format(**data)

        app.logger.debug(f"empty data: {sendEmptyData}")

        parameters = {
            "verify": os.getenv("VERIFY_SSL", "False") == "True"
        }

        if not sendEmptyData:
            parameters["json"] = data

        app.logger.debug("request url: {}".format(url))

        if use_tests_folder:
            req = AttrDict({
                "text": open("tests/{}.json".format(url.split("{}/".format(os.getenv("RDS_INSTALLATION_DOMAIN")))[-1])).read(),
                "status_code": 200,
            })

        else:
            req = getattr(requests, reqConf["method"])(
                url, **parameters
            )

        response = req.text
        app.logger.debug(
            "status_code: {}, content: {}".format(req.status_code, response))

        if req.status_code >= 300:
            return None

        if reqConf["after"] is not None:
            if reqConf["after"].__name__.startswith("refresh"):
                try:
                    reqConf["after"]()
                except:
                    pass
            else:
                try:
                    data = json.loads(
                        response) if not reqConf["giveResponseObject"] else req
                    response = json.dumps(
                        reqConf["after"](data))
                except:
                    pass

        return response


class HTTPManager:
    def __init__(self, socketio):
        self.services = []
        self.socketio = socketio

    def addService(self, service: HTTPRequest):
        if not isinstance(service, HTTPRequest):
            raise ValueError

        self.services.append(service)

        for key in service.requestList.keys():
            def outerFn(key):
                def reqFn(*args):
                    try:
                        return service.makeRequest(key, *args)
                    except Exception as e:
                        app.logger.error(
                            "make request error: {}".format(e), exc_info=True)
                return reqFn

            self.socketio.on_event(key, outerFn(key))

    def makeRequest(self, *args, **kwargs):
        for service in self.services:
            try:
                return service.makeRequest(*args, **kwargs)
            except Exception as e:
                app.logger.error(e, exc_info=True)

        raise ValueError("no service implements the given url.")
