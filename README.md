# AutoJson

A python module that attempts to let classes be serializable without any work

# Usage
```py
from JsonSerialize import *
import json

@JsonSerializable()
class TestClass: 
    def __init__(self, id : int) -> None:
        self.id = id

dump = json.dumps(TestClass(155), default=encoder)
load = json.loads(dump, object_hook=decoder)
print(load.id) # should be 155
```

# Example
```py
from JsonSerialize import JsonSerializable, encoder, decoder
import json

@JsonSerializable() # dont forget the ()
class Mail:
    def __init__(self, content = None):
        self.content = content
    def __repr__(self) -> str: return f"mail: {self.content}"

@JsonSerializable(IGNORE_ATTRIBUTES=[]) # You can provide a list of attributes to ignore when serializing
class User:
    def __init__(self, name, email, inbox = None):
        self.name = name
        self.email = email
        self.inbox : list[Mail] = inbox or []

    def __repr__(self) -> str:
        return f"Name: {self.name} - Email: {self.email}\nInbox: {self.inbox}"

TestUser = User("Test", "test@example.com")
TestUser.inbox.append(Mail(content="hello"))
TestUser.inbox.append(Mail(content="hi!")  )

# dumping object....
Dump : str = json.dumps(TestUser, default=encoder, indent=4) #make sure to include the default=encoder
print(Dump) # now just a string, custom classes in json format contain __class_type__
#

# loading object....
Loaded : User = json.loads(Dump, object_hook=decoder) # make sure to include the object_hook=decoder
print(Loaded) # now back to a custom object
```

#### note: if you want it to encode to a dictionary instead so you can save it to something mongoDB just do `encoder(obj, DictForm=True)`
