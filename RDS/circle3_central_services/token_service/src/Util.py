from lib.Storage import Storage
import importlib, json

# singleton storage
storage = None

def load_class_from_json(jsonStr: str):
    """
    Returns the class of the given json string.
    """
    data = json.loads(jsonStr)
    return internal_load_class(data)

def load_class_from_dict(data: dict):
    """
    Returns the class of the given dict.
    """
    return internal_load_class(data)

def internal_load_class(data: dict):
    """
    For internal use only.
    """
    if "type" in data:
        if data["type"].endswith("Token"):
            try:
                mod = importlib.import_module('lib.Token')
                TokenType = getattr(mod, data["type"])
                return TokenType
            except Exception:
                raise

        raise ValueError("given data not a valid class.")
    raise ValueError("Type not specified in data.")