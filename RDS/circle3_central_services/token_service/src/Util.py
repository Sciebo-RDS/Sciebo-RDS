from lib.Storage import Storage
    
import importlib, json

# singleton storage
storage = None

def load_class_from_json(jsonStr: str):
    """
    Returns the class of the given json string.
    """

    if not isinstance(jsonStr, str):
        raise ValueError("Given parameter not a string.")

    data = jsonStr

    while not isinstance(data, dict): # FIX for json bug: Sometimes it returns a string.
        data = json.loads(data)

    return internal_load_class(data)

def load_class_from_dict(data: dict):
    """
    Returns the class of the given dict.
    """
    return internal_load_class(data)

def initialize_object_from_json(jsonStr: str):
    """
    Initialize and returns an object of the given json string.

    This is the easiest way to reverse the __json__ method for objects from our lib folder.
    """
    return load_class_from_json(jsonStr).from_json(jsonStr)

def internal_load_class(data: dict):
    """
    For internal use only.
    """

    if not isinstance(data, dict):
        raise ValueError("Given parameter not a dict object.")

    if "type" in data:
        try:
            klass = None
            if data["type"].endswith("Token"):
                mod = importlib.import_module('lib.Token')
                klass = getattr(mod, data["type"])
            elif data["type"].endswith("Service"):
                mod = importlib.import_module('lib.Service')
                klass = getattr(mod, data["type"])
            elif data["type"].endswith("User"):
                mod = importlib.import_module('lib.User')
                klass = getattr(mod, data["type"])

            if klass is not None:
                return klass
        except Exception:
            raise

        raise ValueError("given parameter not a valid class.")
    raise ValueError("Type not specified in parameter.")