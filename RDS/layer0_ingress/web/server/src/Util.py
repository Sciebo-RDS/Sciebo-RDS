
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


def listContainsService(arr: list, service: dict) -> bool:

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


def removeDuplicates(response: list) -> list:
    """Removes duplicate entries of equal servicenames

    Args:
        response (list): list of service entries

    Returns:
        Same as response, but duplicates removed.
    """
    withoutDuplicates = []
    for service in response:
        if not listContainsService(withoutDuplicates, service):
            withoutDuplicates.append(service)
    return withoutDuplicates

def applyFilters(response: list, helperSession=None) -> list:
    """Applies filters for services

    Args:
        response (list): Take a look into openapi spec for services properties.
        filters (list): List of Dicts. Expected fieldnames in dict: `name` for servicename to filter, `only` for domainnames and `except` same as `only`.
    
    Returns:
        Filtered services, if domains said to do.
    """
    
    if helperSession is not None:
        session = helperSession
    else:
        from flask import session
    
    result = response
    filters = session["oauth"]
    
    if "filters" in filters:
        filters = session["oauth"]["filters"]
        onlyFiltered = []
        
        
        if "only" in filters and len(filters["only"]) > 0:
            onlyFiltered = [service for service in response if service["informations"]["servicename"] in filters["only"]]
        else:
            onlyFiltered = response
        
        if "except" in filters and len(filters["except"]) > 0:
            exceptFiltered = [service for service in onlyFiltered if service["informations"]["servicename"] not in filters["except"]]
        else:
            exceptFiltered = onlyFiltered
            
        result = exceptFiltered
    
    session["servicelist"] = result
    return result
    
def isServiceInLastServicelist(servicename: str, helperSession=None) -> bool:
    """Checks if servicename was in latest servicelist response for the current session.

    Args:
        servicename (_type_): The servicename yo want to know, if it is in latest servicelist.
        helperSession (_type_, optional): Use this session for unittests. Defaults to None.

    Returns:
        bool: True, if servicename was in latest servicelist response.
    """
    
    if helperSession is not None:
        session = helperSession
    else:
        from flask import session
        
    if isinstance(servicename, dict):
        servicename = servicename["servicename"]
    servicelist = session["servicelist"]
    
    found_service = [servicename == service["informations"]["servicename"] for service in servicelist]
    result = "servicelist" in session and any(found_service)
    
    return result
    
