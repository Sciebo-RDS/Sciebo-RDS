
import copy
import json


def checkForEmpty(response):
    if response.status_code == 404:
        return []
    else:
        return parseAllResearch(json.loads(response.text))


def parsePropBack(prop):
    types = ["fileStorage", "metadata"]

    data = [
        {"portType": typ, "value": True}
        for typ in types
        if typ in prop["type"]
    ]

    customProp = [{"key": key, "value": value}
                  for key, value in prop.get("customProperties", {}).items()]

    if len(customProp) > 0:
        data.append({"portType": "customProperties", "value": customProp})

    return data


def parsePortBack(port):
    return {
        "port": port["port"],
        "properties": parsePropBack(port["properties"])
    }


def parseResearchBack(response):
    data = {
        "portIn": [parsePortBack(port) for port in response["portIn"]],
        "portOut": [parsePortBack(port) for port in response["portOut"]]
    }
    d = copy.deepcopy(response)
    d.update(data)
    return d


def parseCustomProp(customProp):
    return {val["key"]: val["value"] for val in customProp}


def parseProp(prop):
    propList = {"type": []}
    for val in prop:
        if val["portType"] == "customProperties":
            propList["customProperties"] = parseCustomProp(val["value"])
        else:
            propList["type"].append(val["portType"])
    return propList


def parsePort(port):
    return {
        "port": port["port"],
        "properties": parseProp(port["properties"])
    }


def parseResearch(response):
    data = {
        "portIn": [parsePort(port) for port in response["portIn"]],
        "portOut": [parsePort(port) for port in response["portOut"]]
    }
    d = copy.deepcopy(response)
    d.update(data)
    return d


def parseAllResearch(response):
    return [parseResearch(research) for research in response]


def parseAllResearchBack(response):
    return [parseResearchBack(research) for research in response]


def listContainsService(arr, service):
    for el in arr:
        try:
            if el["servicename"] == service["servicename"]:
                return True
        except Exception as e:
            pass

        try:
            if el["informations"]["servicename"] == service["informations"]["servicename"]:
                return True
        except Exception as e:
            pass

    return False


def removeDuplicates(response):
    withoutDuplicates = []
    for service in response:
        if not listContainsService(withoutDuplicates, service):
            withoutDuplicates.append(service)
    return withoutDuplicates
