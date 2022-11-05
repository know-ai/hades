# -*- coding: utf-8 -*-
"""pyhades/models.py

This module implements a Tags and other classes for
modelling the subjects involved in the core of the engine.
"""
from inspect import ismethod
import os
import requests
from .utils import logging_error_handler

FLOAT = "float"
INTEGER = "int"
BOOL = "bool"
STRING = "str"



class PropertyType:

    """
    Implement an abstract property type
    """

    def __init__(self, _type, default=None, unit=None, log:bool=False):
        
        self.tag_engine = None
        self._type = _type
        self.unit = unit
        self.__default = default
        self.__value = default
        self.__sio = None
        self.__log = log
        self.__tag_name = None
        self.DAQ_SERVICE_HOST = os.environ.get('DAQ_SERVICE_HOST') or "127.0.0.1"
        self.DAQ_SERVICE_PORT = os.environ.get('DAQ_SERVICE_PORT') or "5001"
        self.DAQ_SERVICE_URL = f"http://{self.DAQ_SERVICE_HOST}:{self.DAQ_SERVICE_PORT}"

    @property
    def value(self):
        r"""
        Documentation here
        """
        return self.__value

    @value.setter
    @logging_error_handler
    def value(self, value):
        
        if self.__value!=value:

            if self.__sio is not None:

                if self.is_logged():
                    payload = {
                        'name': self.tag_name,
                        'value': value
                    }
                    requests.post(f'{self.DAQ_SERVICE_URL}/api/tags/write', json=payload)
                    
                self.__sio.emit("notify_machine_attr", self.__machine.serialize())

            self.__value = value

    def init_socketio(self, machine):
        r"""
        Documentation here"""

        from .core import PyHades
        app = PyHades()

        self.__sio = app.get_socketio()
        self.__machine = machine

    @property
    def tag_name(self):

        return self.__tag_name
    
    @tag_name.setter
    def tag_name(self, tag_name:str):
        
        self.__tag_name = tag_name

    def is_logged(self):
        r"""
        Documentation here
        """

        return self.__log == True

    def set_log(self):
        r"""
        Documentation here
        """
        self.__log = True

    def drop_log(self):
        r"""
        Documentation here
        """
        self.__log = False


class StringType(PropertyType):

    """
    Implement a Float Type
    """

    def __init__(self, default=None, unit=None, log:bool=False):

        super(StringType, self).__init__(STRING, default, unit, log)


class FloatType(PropertyType):

    """
    Implement a Float Type
    """

    def __init__(self, default=None, unit=None, log:bool=False):

        super(FloatType, self).__init__(FLOAT, default, unit, log)


class IntegerType(PropertyType):

    """
    Implement an Integer Typle
    """

    def __init__(self, default=None, unit=None, log:bool=False):

        super(IntegerType, self).__init__(INTEGER, default, unit, log)

        
class BooleanType(PropertyType):

    """
    Implement a Boolean Type
    """

    def __init__(self, default=None, unit=None, log:bool=False):

        super(BooleanType, self).__init__(BOOL, default, unit, log)


class Model(object):

    """
    Implement an abstract model for inheritance
    """

    def __init__(self, **kwargs):

        attrs = self.get_attributes()

        for key, value in attrs.items():
            
            if key in kwargs:
                default = kwargs[key]
            else:
                try:
                    default = value.default
                    _type = value._type
                    
                except Exception as e:
                    continue

            if default:
                setattr(self, key, default)
            else:
                if _type == FLOAT:
                    setattr(self, key, 0.0)
                elif _type == INTEGER:
                    setattr(self, key, 0)
                elif _type == BOOL:
                    setattr(self, key, False)
                elif _type == STRING:
                    setattr(self, key, "")

        self.attrs = attrs

    def __getattribute__(self, attr):
        
        method = object.__getattribute__(self, attr)
        
        if not method:
            return method

        if callable(method):
             
            def new_method(*args, **kwargs):
                 
                result = method(*args, **kwargs)
                name = method.__name__

                if ("__" not in name) and (name != "save"):
                    try:
                        self.save()
                    except Exception as e:
                        pass

                return result
            return new_method
        else:
            return method

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    @classmethod
    def get_attributes(cls):

        result = dict()
        
        props = cls.__dict__

        for key, value in props.items():
            
            if hasattr(value, '__call__'):
                continue
            if isinstance(value, cls):
                continue
            if not ismethod(value):

                if "__" not in key:
                    result[key] = value

        return result
    
    def commit(self):

        from .tags.cvt import CVTEngine

        _cvt = CVTEngine()
        
        try:
            _cvt.write_tag(self.tag, self)
            return True
        except Exception as e:
            return False

    def set_attr(self, name, value):
        
        setattr(self, name, value)

    def get_attr(self, name):

        result = getattr(self, name)
        return result

    @classmethod
    def set(cls, tag, obj):

        obj.tag = tag

    @classmethod
    def get(cls, tag):

        from .tags.cvt import CVTEngine

        _cvt = CVTEngine()

        return _cvt.read_tag(tag)

    def save(self):

        from .tags.cvt import CVTEngine

        _cvt = CVTEngine()

        try:
            tag = self.tag

            _cvt.write_tag(tag, self)
        except Exception as e:
            raise KeyError

    def serialize(self):

        result = dict()

        attrs = self.get_attributes()

        for key in attrs:
            value = getattr(self, key)
            result[key] = value

        return result

    def _load(self, values):

        for key, value in values.items():

            setattr(self, key, value)