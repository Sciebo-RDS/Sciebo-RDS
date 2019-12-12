import os,sys
sys.path.append(f"{os.getcwd()}/src") # for connexion

from json import JSONEncoder, JSONDecoder


def to_default(self, obj):
    return getattr(obj.__class__, "to_json", to_default.default)(obj)


to_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = to_default  # Replace it.