import typing as t
import json
import sys

T = t.TypeVar('T', bound='MyObject')

class MyObject(object):

    def __init__(self, **entries):
        self.__dict__.update(entries)
        
    @staticmethod
    def from_dict(dictionary: t.Dict, clazz: T) -> T:
        return clazz(**dictionary)
    @staticmethod
    def from_json(json_string: str, clazz: T) -> T:
        return json.loads(
            json_string, 
            object_hook= lambda dict: FileApplicationObject.from_dict(dict, clazz))
    @staticmethod
    def from_json_bytes(self, json_as_bytes: str) -> T:
        return FileApplicationObject.from_json(json_as_bytes.decode())
    def to_json(self) -> str:
        return json.dumps(self.__dict__, 
            indent=None, separators=(',', ':'))
    
    def to_json_bytes(self, encoding: str = sys.getdefaultencoding()) -> str:
        return self.to_json().encode(encoding)