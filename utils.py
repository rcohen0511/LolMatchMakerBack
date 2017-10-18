import json

from bson.objectid import ObjectId
from datetime import datetime

def to_json(obj, pretty=True):
    class DefaultEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            if isinstance(o, datetime):
                return str(o)
            return o.__dict__

    # return json.dumps(cls=DefaultEncoder, obj=obj, indent=2 if pretty else None, sort_keys=True)
    return json.dumps(cls=DefaultEncoder, obj=obj, indent=2 if pretty else None)


def from_json(str):
    return json.loads(str)


def norm_json(s):
    return from_json(to_json(s))