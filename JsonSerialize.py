from __future__ import annotations
import json
IGNORES = (dict, list, set)
__loads__ = json.loads
__dumps__ = json.dumps
def encoder(obj : object, DictForm=True):
    partially_encoded = __encoder__(obj)
    if DictForm: return partially_encoded
    return __dumps__(partially_encoded)

def __encoder__(obj : object):
    if hasattr(obj,"ToDict"):
        return obj.ToDict()
    else:
        if isinstance(obj, IGNORES):
            if isinstance(obj, dict):
                new_obj = {}
                for i in obj:
                    new_obj[__encoder__(i)] = __encoder__(obj[i])
                return new_obj
            return obj.__class__([__encoder__(i) for i in obj])
        return obj

SERIALIZABLE_CLASSES : dict = dict()
def JsonSerializable(IGNORE_ATTRIBUTES = None):
    IGNORE_ATTRIBUTES = IGNORE_ATTRIBUTES or []
    def Decorator(cls):
        def ToDict(self):
            result = {}
            result["__CLASS_TYPE__"] = cls.__name__
            search_list = []
            if hasattr(self, "__dict__"): search_list += vars(self)
            elif hasattr(self, "__slots__"): search_list += self.__slots__
            for variable in search_list:
                if variable not in IGNORE_ATTRIBUTES:
                    attr = getattr(self, variable)
                    result[__encoder__(variable)] = __encoder__(attr)
            return result
        def FromDict(obj):
            for key, value in obj.items():
                if not isinstance(value, IGNORES): continue
                obj[key] = decoder(value)
            print(obj)
            return cls(**obj)
        if not hasattr(cls, 'ToDict'): cls.ToDict = ToDict
        if not hasattr(cls, 'FromDict'): cls.FromDict = FromDict
        SERIALIZABLE_CLASSES[cls.__name__] = cls
        return cls
    return Decorator

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
        return cls.FromDict(obj)

    elif isinstance(obj, (list,set)):
        result = obj.__class__([decoder(i) for i in obj])
        return result
    return obj
