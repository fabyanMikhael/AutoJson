from __future__ import annotations
import json

def encoder(obj : object):
    if "ToDict" in dir(obj):
        return obj.ToDict()
    else:
        return json.dumps(obj)

SERIALIZABLE_CLASSES : dict = dict()
def JsonSerializable(IGNORE_ATTRIBUTES = None):
    IGNORE_ATTRIBUTES = IGNORE_ATTRIBUTES or []
    def Decorator(cls):
        def ToDict(self):
            result = {}
            result["__CLASS_TYPE__"] = cls.__name__
            SERIALIZABLE_CLASSES[cls.__name__] = cls
            for variable in vars(self):
                if variable not in IGNORE_ATTRIBUTES:
                    result[variable] = getattr(self, variable)
            return result
        cls.ToDict = ToDict
        return cls
    return Decorator

__loads__ = json.loads
IGNORES = (dict, list, set)
def decoder(string, *args, **kwargs):
    if isinstance(string, IGNORES):
        obj = string
    else :
        obj = __loads__(string, *args, **kwargs)
    if isinstance(obj, dict) and "__CLASS_TYPE__" in obj:
        cls = obj["__CLASS_TYPE__"]
        if not cls in SERIALIZABLE_CLASSES: raise TypeError(f"class {cls} is *not* loaded yet!")
        cls = SERIALIZABLE_CLASSES[obj["__CLASS_TYPE__"]]
        obj.pop("__CLASS_TYPE__")
        for key, value in obj.items():
            if not isinstance(value, IGNORES): continue
            obj[key] = decoder(value)
        return cls(**obj)
    return obj