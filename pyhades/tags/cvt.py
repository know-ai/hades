# -*- coding: utf-8 -*-
"""pyhades/tags/cvt.py

This module implements a Current Value Table (CVT), for holding current
tag values, in a thread safe implementation for Data Acquisition,
Database logging, Math operations and others real time processes.
"""
import threading
import copy
from datetime import datetime
import yaml
from .._singleton import Singleton
from .tag import Tag
from ..logger import DataLoggerEngine
from ..dbmodels import Tags
import yaml
from ..utils import log_detailed


class CVT:
    """Current Value Table class for Tag based repository.

    This class is intended hold in memory tag based values and 
    observers for those required tags, this class is intended to be
    used by PyHades itself and not for other purposes

    Usage:
    
    ```python
    >>> from pyhades.tags import CVT
    >>> _cvt = CVT()
    ```

    """

    logger = DataLoggerEngine()

    def __init__(self):

        self._tags = dict()
        self.data_types = ["float", "int", "bool", "str"]

    def set_data_type(self, data_type):

        self.data_types.append(data_type)
        self.data_types = list(set(self.data_types))

    def tag_defined(self, name):

        return name in self._tags.keys()

    def set_tag(
        self, 
        name:str, 
        unit:str, 
        data_type:str, 
        desc:str="", 
        min_value:float=None, 
        max_value:float=None,
        tcp_source_address:str=None,
        node_namespace:str=None):
        """Initialize a new Tag object in the _tags dictionary.
        
        # Parameters
        name (str):
            Tag name.
        data_type (str): 
            Tag value type ("int", "float", "bool", "str")
        """

        if isinstance(data_type, str):
        
            if data_type in self.data_types:
                if data_type == "float":
                    value = 0.0
                elif data_type == "int":
                    value = 0
                elif data_type == "str":
                    value = ""
                else:
                    value = False

        else:
            value = data_type()
            data_type.set(name, value)
            data_type = data_type.__name__
            self.set_data_type(data_type)

        tag = Tag(name, unit, data_type, desc, min_value, max_value, tcp_source_address, node_namespace)

        tags = Tags.create(
                name=name, 
                unit=unit, 
                data_type=data_type,
                desc=desc,
                min_value=min_value,
                max_value=max_value,
                tcp_source_address=tcp_source_address,
                node_namespace=node_namespace
            )

        self._tags[name] = tag

    def set_tags(self, tags):
        """Initialize a list of new Tags object in the _tags dictionary.
        
        # Parameters
        tags (list):
            List of (tag, _type).
        """
        for name, data_type in tags:
            
            self.set_tag(name, data_type)

    def get_tags(self):
        """Returns a list of the defined tags names.
        """
        
        return {key: value.get_attributes() for key, value in self._tags.items()}

    def get_tag_by_node_namespace(self, node_namespace):
        r"""
        Documentation here
        """
        for tag_name, tag in self._tags.items():

            if tag.get_node_namespace()==node_namespace:

                return tag_name

        return None

    def get_node_namespace_by_tag_name(self, name):
        r"""
        Documentation here
        """
        for tag_name, tag in self._tags.items():

            if tag_name==name:

                return tag.get_node_namespace()

        return None

    def set_value(self, name, value):
        """Sets a new value for a defined tag.
        
        # Parameters
        name (str):
            Tag name.
        value (float, int, bool): 
            Tag value ("int", "float", "bool")
        """

        if "." in name:
            values = name.split(".")
            tag_name = values[0]
        else:
            tag_name = name
        
        if tag_name not in self._tags:
            raise KeyError

        if "." in name:
            values = name.split(".")
            name = values[0]
            _property = values[1]
            setattr(self._tags[name].value, _property, value)
            self._tags[name].notify()

        else:
            # self._tags[name]['value']['value'] = value
            self._tags[name].set_value(value)
        
        self.logger.write_tag(tag_name, value)

    def get_value(self, name):
        """Returns a tag value defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        
        if "." in name:
            values = name.split(".")
            name = values[0]
            _property = values[1]
            _new_object = copy.copy(getattr(self._tags[name].value, _property))
        else:
            # _new_object = copy.copy(self._tags[name]['value']['value'])
            _new_object = copy.copy(self._tags[name].get_value())
        
        return _new_object

    def get_data_type(self, name):
        """Returns a tag type defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """

        return self._tags[name].get_data_type()

    def get_attributes(self, name):
        """Returns a tag type defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """

        return self._tags[name].get_attributes()

    def get_unit(self, name):

        """Returns the units defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """

        return self._tags[name].get_unit()

    def get_description(self, name):

        """Returns the description defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """

        return self._tags[name].get_description()

    def get_min_value(self, name):

        """Returns the tag min value defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """

        return self._tags[name].get_min_value()

    def get_max_value(self, name):

        """Returns the tag max value defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """

        return self._tags[name].get_max_value()

    def get_data_types(self):
        """Returns all tag types.
        
        # Parameters
        """

        return self.data_types

    def attach_observer(self, name, observer):
        """Attaches a new observer to a tag object defined by name.
        
        # Parameters
        name (str):
            Tag name.
        observer (TagObserver): 
            Tag observer object, will update once a tag object is changed.
        """

        self._tags[name].attach(observer)

    def detach_observer(self, name, observer):
        """Detaches an observer from a tag object defined by name.
        
        # Parameters
        name (str):
            Tag name.
        observer (TagObserver): 
            Tag observer object.
        """
        self._tags[name].attach(observer)


class CVTEngine(Singleton):
    """Current Value Table Engine class for Tag thread-safe based repository.

    This class is intended hold in memory tag based values and 
    observers for those required tags, it is implemented as a singleton
    so each sub-thread within the PyHades application can access tags
    in a thread-safe mechanism.

    Usage:
    
    ```python
    >>> from pyhades.tags import CVTEngine
    >>> tag_egine = CVTEngine()
    ```

    """

    def __init__(self):

        super(CVTEngine, self).__init__()

        self._cvt = CVT()
        self._groups = dict()
        self._request_lock = threading.Lock()
        self._response_lock = threading.Lock()
        self._config = None
        self.__tags = list()
        self._response = None

        self._response_lock.acquire()

    def set_config(self, config_file):
        r"""
        Documentaion here
        """
        with open(config_file) as f:
            
            self._config = yaml.load(f, Loader=yaml.FullLoader)

            if self._config['modules'] is not None:

                if 'tags' in self._config['modules']:

                    if self._config['modules']['tags'] is not None:

                        if 'groups' in self._config['modules']['tags']:

                            groups = self._config['modules']['tags']['groups']
                            self.__set_config_groups(groups)

                        else:

                            tags = self._config['modules']['tags']
                            __tags = self.__set_config_tags(tags)

                            self.set_tags(__tags)

    def __set_config_groups(self, groups):
        r"""
        Documentation here
        """                
        for group, _tags in groups.items():

            __tags = self.__set_config_tags(_tags)
            
            self.set_group(group, *__tags)

    def __set_config_tags(self, tags):
        r"""
        Documentaion here
        """
        __tags = list()
        for _, attrs in tags.items():

            _tag = Tag(**attrs)

            __tags.append(_tag.parser())
            
        self.__tags.extend(__tags)

        return __tags

    def set_data_type(self, data_type):
        r"""
        Sets a new data_type as string format.
        
        **Parameters:**
        * **data_type** (str): Data type.

        **Returns** `None`

        """
        if data_type not in self._cvt.get_data_types():
            self._cvt.set_data_type(data_type)

    def load_tag_from_db_to_cvt(self):
        r"""
        Documentation here
        """
        db_tags = Tags.read_all()
        cvt_tags = self.get_tags()

        for db_tag in db_tags['data']:

            if db_tag not in list(cvt_tags.keys()):
                
                db_tag.pop('id')
                self.set_tag(**db_tag)
            

    def get_data_type(self, name):
        """
        Gets a tag data type as string format.
        
        **Parameters:**

        * **name** (str): Tag name.

        **Returns**

        * **(str)**
        ```python
        >>> tag_egine.get_data_type('TAG1')
        ```
        """

        return self._cvt.get_data_type(name)

    def get_unit(self, name):
        """
        Gets the units defined for a tag.
        
        **Parameters:**
        
        * **name** (str): Tag name.
        """

        return self._cvt.get_unit(name)

    def get_description(self, name):
        """
        Gets the descriptions defined for a tag.
        
        **Parameters:**
        
        * **name** (str): Tag name.
        """

        return self._cvt.get_description(name)

    def get_min_value(self, name:str):

        return self._cvt.get_min_value(name)

    def get_max_value(self, name):

        return self._cvt.get_max_value(name)

    def get_tagname_by_node_namespace(self, node_namespace:str):
        r"""
        Documentation here
        """
        return self._cvt.get_tag_by_node_namespace(node_namespace)

    def get_node_namespace_by_tag_name(self, name:str):
        r"""
        Documentation here
        """
        return self._cvt.get_node_namespace_by_tag_name(name)

    def tag_defined(self, name):
        """
        Checks if a tag name is already defined.
        
        **Parameters:**

        * **name** (str): Tag name.
        """

        return self._cvt.tag_defined(name)

    def set_tag(
        self, 
        name:str, 
        unit:str, 
        data_type:str, 
        desc="", 
        min_value=None, 
        max_value=None,
        tcp_source_address=None,
        node_namespace=None):
        """
        Sets a new value for a defined tag, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag name.
        * **unit** (str): Engineering units.
        * **data_type** (float, int, bool): Tag value ("int", "float", "bool")
        * **desc** (str): Tag description
        * **min_value** (int - float): Field instrument lower value
        * **max_value** (int - float): Field instrument higher value

        Usage:
    
        ```python
        >>> tag_engine.set_tag("speed", "float", "km/h", "Speed of car", 0.0, 240.0)
        ```
        """
        
        if not self.tag_defined(name):

            self._cvt.set_tag(name, unit, data_type, desc, min_value, max_value, tcp_source_address, node_namespace)

    def set_tags(self, tags):
        """
        Sets new values for a defined list of tags, 
        in thread-safe mechanism.
        
        **Parameters:**
        
        * **tags** (list): List of tag name, unit, data type, description, min and max value

        ```python
        >>> tags = [
                ("TAG1", 'ºC', 'float', 'Inlet temperature', 0.0, 100.0),
                ("TAG2", 'kPa', 'float', 'Inlet pressure', 100.0),
                ("TAG3", 'm3/s', 'float', 'Inlet flow'),
                ("TAG4", 'kg/s', 'float')
            ]
        >>> tag_engine.set_tags(tags)
        ```
        """
        for tag_attrs in tags:

            if len(tag_attrs) >= 3:

                self.set_tag(*tag_attrs)

    def set_group(self, group, *tags):
        """
        Sets new tags group, which can be retrieved
        by group name.
        
        **Parameters:**
        
        * **group** (str): Group name.
        * **tags** (list): List of defined tag names.

        ```python
        >>> temp_tags = [
                ("TAG1", 'ºC', 'float', 'Inlet temperature', 0.0, 100.0),
                ("TAG2", 'ºC', 'float', 'Outlet temperature', 0.0, 100.0)
            ]
        >>> pressure_tags = [
                ("TAG3", 'kPa', 'float', 'Inlet pressure', 100.0, 200.0),
                ("TAG4", 'kPa', 'float', 'Outlet pressure', 0.0, 100.0)
            ]
        >>> tag_engine.set_group('Temperatures', temp_tags)
        >>> tag_engine.set_group('Pressures', pressure_tags)
        ```
        """

        self._groups[group] = list()

        for attrs in tags:
            name = attrs[0]
            self._groups[group].append(name)

        self.set_tags(tags)

    def get_group(self, group):
        """
        Returns the tag list of the a defined group.
        
        **Parameters:**
        
        * **group** (list of str): Group name.
        ```python
        >>> tag_engine.get_group('Temperatures')
        ['TAG1', 'TAG2']
        >>> tag_engine.get_group('Pressures')
        ['TAG3', 'TAG4']
        ```
        """

        return self._groups[group]

    def get_groups(self):
        """
        Returns a list of the group names defined.
        """

        return list(self._groups.keys())

    def get_tags(self):
        """
        Returns a list of the tag names defined.
        """

        return self._cvt.get_tags()

    def write_tag(self, name, value):
        """
        Writes a new value for a defined tag, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag name.
        * **value** (float, int, bool, str):  Tag value ("int", "float", "bool", "str")
        ```python
        >>> tag_engine.write_tag('TAG1', 50.53)
        ```
        """

        _query = dict()
        _query["action"] = "set_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name
        _query["parameters"]["value"] = value

        self.request(_query)
        result = self.response()

        return result

    def read_tag(self, name):
        """
        Returns a tag value defined by name, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag name.

        ```python
        >>> tag_engine.read_tag('TAG1')
        50.53
        ```
        """

        _query = dict()
        _query["action"] = "get_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def attach(self, name, observer):
        """
        Attaches an observer object to a Tag, observer gets notified when the Tag value changes.
        
        **Parameters:**

        * **name** (str): Tag name.
        * **observer** (str): TagObserver instance.
        """

        _query = dict()
        _query["action"] = "attach"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name
        _query["parameters"]["observer"] = observer

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def detach(self, name, observer):
        """
        Detaches an observer object from a Tag, observer no longer gets notified when the Tag value changes.
        
        **Parameters:**

        * **name** (str): Tag name.
        * **observer** (str): TagObserver instance.
        """
        
        _query = dict()
        _query["action"] = "detach"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name
        _query["parameters"]["observer"] = observer

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_data_type(self, name):
        """
        Returns a tag type defined by name, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag name.
        """

        _query = dict()
        _query["action"] = "get_data_type"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            
            return result["response"]

    def read_unit(self, name):
        """
        Returns the units defined for a tag name, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.
        """

        _query = dict()
        _query["action"] = "get_unit"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_description(self, name):
        """
        Returns the description defined for a tag name, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.
        """

        _query = dict()
        _query["action"] = "get_description"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_min_value(self, name):
        """
        Returns the min value defined for a tag name, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.
        """

        _query = dict()
        _query["action"] = "get_min_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_max_value(self, name):
        """
        Returns the max value defined for a tag name, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.
        """

        _query = dict()
        _query["action"] = "get_max_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_attributes(self, name):
        """
        Returns all attributes defined for a tag name, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        ```python
        >>> tag_engine.read_attributes('TAG1')
        {
            "value":{
                    "status_code":{
                    "name": 'GOOD',
                    "value": '0x000000000',
                    "description":  'Operation succeeded'
                },
                "source_timestamp": '03/25/2022, 14:39:29.189422',
                "value": 50.53,
            },
            'name': 'TAG1', 
            'unit': 'ºC', 
            'data_type': 'float', 
            'description': 'Inlet temperature', 
            'min_value': 0.0, 
            'max_value': 100.0
        }
        ```
        """

        _query = dict()
        _query["action"] = "get_attributes"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def request(self, _query):

        self._request_lock.acquire()

        action = _query["action"]

        if action == "set_tag":

            try:
                parameters = _query["parameters"]

                name = parameters["name"]
                data_type = parameters["data_type"]

                self._cvt.set_tag(name, data_type)
                self._response = {
                    "result": True
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False
                }
        
        elif action == "get_tags":

            try:

                tags = self._cvt.get_tags()

                self._response = {
                    "result": True,
                    "response": tags
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_value":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = self._cvt.get_value(name)

                self._response = {
                    "result": True,
                    "response": value
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_data_type":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = self._cvt.get_data_type(name)

                self._response = {
                    "result": True,
                    "response": value
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_unit":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = self._cvt.get_unit(name)

                self._response = {
                    "result": True,
                    "response": value
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_description":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = self._cvt.get_description(name)

                self._response = {
                    "result": True,
                    "response": value
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_min_value":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = self._cvt.get_min_value(name)

                self._response = {
                    "result": True,
                    "response": value
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_max_value":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = self._cvt.get_max_value(name)

                self._response = {
                    "result": True,
                    "response": value
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "get_attributes":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                attrs = self._cvt.get_attributes(name)

                self._response = {
                    "result": True,
                    "response": attrs
                }
            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False,
                    "response": None
                }

        elif action == "set_value":

            try:

                parameters = _query["parameters"]

                name = parameters["name"]
                value = parameters["value"]
                self._cvt.set_value(name, value)
                self._response = {
                    "result": True
                }

            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False
                }
        
        elif action in ("attach", "detach"):

            try:
                parameters = _query["parameters"]
                name = parameters["name"]
                observer = parameters["observer"]
                
                if action == "attach":
                    self._cvt.attach_observer(name, observer)
                else:
                    self._cvt.detach_observer(name, observer)

                self._response = {
                    "result": True
                }

            except Exception as e:
                message = "Error in CVTEngine"
                log_detailed(e, message)
                self._response = {
                    "result": False
                }
                
        self._response_lock.release()

    def response(self):

        self._response_lock.acquire()

        result = self._response

        self._request_lock.release()

        return result

    def serialize_tag(self, tag):

        attrs = self.read_attributes(tag)

        try:
            result = attrs
        except:
            result = {
                'tag': tag
            }

        return result

    def serialize(self):

        result = list()

        tags = self.get_tags()

        for _tag in tags:

            record = self.serialize_tag(_tag)

            result.append(record)

        return result

    def serialize_group(self, name):

        result = list()

        tags = self.get_group(name)

        for _tag in tags:

            record = self.serialize_tag(_tag)

            result.append(record)

        return result

    def __getstate__(self):

        self._response_lock.release()
        state = self.__dict__.copy()
        del state['_request_lock']
        del state['_response_lock']
        return state

    def __setstate__(self, state):
        
        self.__dict__.update(state)
        self._request_lock = threading.Lock()
        self._response_lock = threading.Lock()

        self._response_lock.acquire()
