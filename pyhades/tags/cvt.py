# -*- coding: utf-8 -*-
"""pyhades/tags/cvt.py

This module implements a Current Value Table (CVT), for holding current
tag values, in a thread safe implementation for Data Acquisition,
Database logging, Math operations and others real time processes.
"""
import threading
import copy
import yaml
import json
from .._singleton import Singleton
from .tag import Tag
from ..logger import DataLoggerEngine
from ..dbmodels import Tags, Variables, Units
import yaml
from ..utils import log_detailed
from .unit_conversion import UnitConversion


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
    unit_converter = UnitConversion
    

    def __init__(self):

        self._tags = dict()
        self.data_types = ["float", "int", "bool", "str"]

    def set_data_type(self, data_type):

        self.data_types.append(data_type)
        self.data_types = list(set(self.data_types))

    def tag_defined(self, name):

        for id, value in self._tags.items():
            
            if name == value.name:

                return True

        return False

    def set_tag(
        self, 
        name:str, 
        unit:str, 
        data_type:str, 
        description:str, 
        min_value:float=None, 
        max_value:float=None,
        tcp_source_address:str="",
        node_namespace:str=""):
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

        tag = Tag(name, unit, data_type, description, min_value, max_value, tcp_source_address, node_namespace)

        Tags.create(
            name=name, 
            unit=unit, 
            data_type=data_type,
            description=description,
            min_value=min_value,
            max_value=max_value,
            tcp_source_address=tcp_source_address,
            node_namespace=node_namespace
        )

        _tag = Tags.read_by_name(name)

        if _tag:

            self._tags[str(_tag.id)] = tag

    def set_tags(self, tags):
        """Initialize a list of new Tags object in the _tags dictionary.
        
        # Parameters
        tags (list):
            List of (tag, _type).
        """
        for name, data_type in tags:
            
            self.set_tag(name, data_type)

    def delete_tag(self, name):
        r"""
        Documentation here
        """
        from pyhades import PyHades
        app = PyHades()
        alarm_manager = app.get_alarm_manager()
        tag = Tags.read_by_name(name=name)
        Tags.delete(tag.id)                         # remove from database
        self._tags.pop(str(tag.id))                 # remove from manager

        # Remove alarm related with tag
        alarms = alarm_manager.get_alarms_by_tag(name)

        for id, _ in alarms.items():

            alarm_manager.delete_alarm(id)

    def update_tag(self, id, **kwargs):
        r"""
        Documentation here
        """
        tag = self._tags[id]
        Tags.put(id, **kwargs)
        tag.update(**kwargs)
        self._tags[id] = tag
        return Tags.read(id)

    def get_tags(self):
        """Returns a list of the defined tags names.
        """
        
        return {key: value.get_attributes() for key, value in self._tags.items()}

    def get_tag_by_node_namespace(self, node_namespace):
        r"""
        Documentation here
        """
        for tag_id, tag in self._tags.items():

            if tag.get_node_namespace()==node_namespace:
                
                return tag.name

        return None

    def get_node_namespace_by_tag_name(self, name):
        r"""
        Documentation here
        """
        tag = Tags.read_by_name(name)
        for tag_name, tag in self._tags.items():

            if self._tags[str(tag.id)]['name']==name:

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
        
        tag = Tags.read_by_name(tag_name)

        if str(tag.id) not in self._tags:
            raise KeyError

        if "." in name:
            values = name.split(".")
            name = values[0]
            _property = values[1]
            setattr(self._tags[str(tag.id)].value, _property, value)
            self._tags[str(tag.id)].notify()

        else:
            self._tags[str(tag.id)].set_value(value)
    
        self.logger.write_tag(tag_name, value)

    def get_value(self, name, unit:str=None):
        """Returns a tag value defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        tag = Tags.read_by_name(name)
        
        if "." in name:
            values = name.split(".")
            name = values[0]
            _property = values[1]
            _new_object = copy.copy(getattr(self._tags[str(tag.id)].value, _property))
        else:
            # _new_object = copy.copy(self._tags[str(tag.id)].get_value(unit=unit))
            _new_object = copy.copy(self._tags[str(tag.id)].get_value())

            _tag = self._tags[str(tag.id)]
            _unit = Units.read_by_unit(unit)
            from_unit = Units.read_by_unit(_tag.unit)
            from_unit = from_unit['name']
            value = self._tags[str(tag.id)].get_value()
            if _unit:
                to_unit = _unit['name']
                new_value =  self.unit_converter.convert(value, from_unit=from_unit, to_unit=to_unit)
                _new_object = copy.copy(new_value)
        
        return _new_object

    def get_data_type(self, name):
        """Returns a tag type defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        tag = Tags.read_by_name(name)
        return self._tags[str(tag.id)].get_data_type()

    def get_attributes(self, id:int):
        """Returns a tag type defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        return self._tags[f"{id}"].get_attributes()

    def get_unit(self, name):

        """Returns the units defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        tag = Tags.read_by_name(name)
        return self._tags[str(tag.id)].get_unit()

    def get_description(self, name):

        """Returns the description defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        tag = Tags.read_by_name(name)
        return self._tags[str(tag.id)].get_description()

    def get_min_value(self, name):

        """Returns the tag min value defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        tag = Tags.read_by_name(name)
        return self._tags[str(tag.id)].get_min_value()

    def get_max_value(self, name):

        """Returns the tag max value defined by name.
        
        # Parameters
        name (str):
            Tag name.
        """
        tag = Tags.read_by_name(name)
        return self._tags[str(tag.id)].get_max_value()

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
        tag = Tags.read_by_name(name)
        self._tags[str(tag.id)].attach(observer)

    def detach_observer(self, name, observer):
        """Detaches an observer from a tag object defined by name.
        
        # Parameters
        name (str):
            Tag name.
        observer (TagObserver): 
            Tag observer object.
        """
        tag = Tags.read_by_name(name)
        self._tags[str(tag.id)].detach(observer)


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

    def set_config(self, config_file:str):
        r"""
        Allows to define tags using a YaML file.

        **Parameters:**

        * **config_file** (str): Url where the configuration file is, the configuratio file must have .yml extension.

        **Returns**

        * None
        ```python
        >>> tag_egine.set_config('base_url/config.yml')
        ```

        ## Configuration File Structure

        ```YaML
        version: '3'

        modules:
            tags:

                groups:

                    cvt:

                        PT-01:
                            name: 'PT-01'
                            unit: 'Pa'
                            data_type: 'float'
                            description: 'Inlet Pressure'
                            min_value: 0.00
                            max_value: 100.00
                            tcp_source_address: ''
                            node_namespace: ''
        ```
        """
        with open(config_file) as f:
            
            self._config = yaml.load(f, Loader=yaml.FullLoader)

            if ('modules' in self._config.keys()) and self._config['modules'] is not None:

                if 'tags' in self._config['modules']:

                    if self._config['modules']['tags'] is not None:

                        if 'groups' in self._config['modules']['tags']:

                            groups = self._config['modules']['tags']['groups']
                            self.__set_config_groups(groups)

                        else:

                            tags = self._config['modules']['tags']
                            __tags = self.__set_config_tags(tags)

                            self.set_tags(__tags)

    def __set_config_groups(self, groups:dict):
        r"""
        Defines groups of tags from a config YaML file

        **Parameters:**

        * **groups** (dict): Tags group definition

        ```python
        groups = {
            'group_name': {
                'tag_name_1': {
                    'name': 'PT-01', 
                    'unit': 'Pa', 
                    'data_type': 'float', 
                    'description': 'Inlet Pressure', 
                    'min_value': 0.0, 'max_value': 100.0, 
                    'tcp_source_address': '', 
                    'node_namespace': ''
                }, 
                'tag_name_2': {
                    'name': 'PT-02', 
                    'unit': 'Pa', 
                    'data_type': 'float', 
                    'description': 'Outlet Pressure', 
                    'min_value': 0.0, 
                    'max_value': 100.0, 
                    'tcp_source_address': '', 
                    'node_namespace': ''
                }
            }
        }
        ```

        **Returns**

        * None

        """                
        for group, _tags in groups.items():

            __tags = self.__set_config_tags(_tags)
            
            self.set_group(group, *__tags)

    def __set_config_tags(self, tags:dict)->list:
        """
        Defines tags from a config YaML file

        **Parameters:**

        * **tags** (dict): Tags definition

        ```python
        tags = {
            'tag_name_1': {
                'name': 'PT-01', 
                'unit': 'Pa', 
                'data_type': 'float', 
                'description': 'Inlet Pressure', 
                'min_value': 0.0, 
                'max_value': 100.0, 
                'tcp_source_address': '', 
                'node_namespace': ''
            }, 
            'tag_name_2': {
                'name': 'PT-02', 
                'unit': 'Pa', 
                'data_type': 'float', 
                'description': 'Outlet Pressure', 
                'min_value': 0.0, 
                'max_value': 100.0, 
                'tcp_source_address': '', 
                'node_namespace': ''
            }
        }
        ```

        **Returns**

        * tags: (list) tags list defined

        """ 
        __tags = list()
        for _, attrs in tags.items():

            _tag = Tag(**attrs)

            __tags.append(_tag.parser())
            
        self.__tags.extend(__tags)

        return __tags

    def set_data_type(self, data_type:str):
        r"""
        Sets a new data_type as string format.
        
        **Parameters:**
        * **data_type** (str): Data type.

        **Returns** 

        * None

        """
        if data_type not in self._cvt.get_data_types():
            
            self._cvt.set_data_type(data_type)

    def load_tag_from_db_to_cvt(self):
        r"""
        It's necessary when initialize your app and already exist a database defined with this app, 
        you must load all tag's definition in your database to your Current Value Table (CVT) or tags repository 
        """
        db_tags = Tags.read_all()
        cvt_tags = self.get_tags()

        for db_tag in db_tags:

            if db_tag not in list(cvt_tags.keys()):
                
                db_tag.pop('id')
                self.set_tag(**db_tag)
            
    def get_data_type(self, name:str)->str:
        r"""
        Gets a tag data type as string format.
        
        **Parameters:**

        * **name** (str): Tag name.

        **Returns**

        * **data_type** (str): Tag's data type
        ```python
        >>> tag_egine.get_data_type('TAG1')
        ```
        """

        return self._cvt.get_data_type(name)

    def get_unit(self, name:str)->str:
        r"""
        Gets tag's unit.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **unit** (str): Tag's unit
        """

        return self._cvt.get_unit(name)

    def get_description(self, name:str)->str:
        r"""
        Gets tag's description.
        
        **Parameters:**
        
        * **name** (str): Tag's name.

        **Returns**

        * **description** (str): Tag's description
        """

        return self._cvt.get_description(name)

    def get_min_value(self, name:str)->float:
        r"""
        Gets tag's min value defined.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **min_value** (float) Tag's min value
        """
        return self._cvt.get_min_value(name)

    def get_max_value(self, name:str)->float:
        r"""
        Gets tag's max value defined.
        
        **Parameters:**
        
        * **name** (str): Tag's name.

        **Returns**

        * **max_value** (float): Tag's max value
        """
        return self._cvt.get_max_value(name)

    def get_tagname_by_node_namespace(self, node_namespace:str)->str:
        r"""
        Gets tag's name binded to a tcp node namespace

        **Parameters**

        * **node_namespace** (str): TCP node namespace

        **Returns**

        * **tag_name** (str): Tag's name binded to a tcp node namespace
        """
        return self._cvt.get_tag_by_node_namespace(node_namespace)

    def get_node_namespace_by_tag_name(self, name:str)->str:
        r"""
        Gets tcp node namespace binded to a tag name

        **Parameters**

        * **name** (str): tag name binded to a tcp node namespace

        **Returns**

        * **node_namespace** (str): TCP node namespace
        """
        return self._cvt.get_node_namespace_by_tag_name(name)

    def tag_defined(self, name:str)->bool:
        """
        Checks if a tag name is already defined into database and tags repository.
        
        **Parameters:**

        * **name** (str): Tag name.

        **Returns**

        * **flag** (bool): True if tag is already defined
        """

        return self._cvt.tag_defined(name)

    def update_tag(self, id:int, **kwargs)->dict:
        r"""
        Updates tag's definition attributes

        **Parameters**

        * **id** (int): Tag ID into database
        * **name** (str)[Optional]: New tag name
        * **unit** (str)[Optional]: New tag unit
        * **data_type** (str)[Optional]: New tag data type
        * **description** (str)[Optional]: New tag description
        * **min_value** (float)[Optional]: New tag min value
        * **max_value** (float)[Optional]: New tag max value
        * **tcp_source_address** (str)[Optional]: New tcp source address to tag binding
        * **node_namespace** (str)[Optional]: New tcp node namespace to tag binding

        **Returns**

        * **tag** (dict): Tag definition updated

        """

        return self._cvt.update_tag(id, **kwargs)

    def set_tag(
        self, 
        name:str, 
        unit:str, 
        data_type:str, 
        description:str, 
        min_value:float=None, 
        max_value:float=None,
        tcp_source_address:str="",
        node_namespace:str=""):
        """
        Defines a new tag.
        
        **Parameters:**

        * **name** (str): Tag name.
        * **unit** (str): Engineering units.
        * **data_type** (float, int, bool): Tag value ("int", "float", "bool")
        * **description** (str): Tag description
        * **min_value** (int - float)[Optional]: Field instrument lower value
        * **max_value** (int - float)[Optional]: Field instrument higher value
        * **tcp_source_address** (str)[Optional]: Url for tcp communication with a server.
        * **node_namespace** (str)[Optional]: Node ID or Namespace (OPC UA) to get element value from server.

        Usage:
    
        ```python
        >>> tag_engine.set_tag("speed", "float", "km/h", "Speed of car", 0.0, 240.0)
        ```
        """
        
        if not self.tag_defined(name):

            self._cvt.set_tag(name, unit, data_type, description, min_value, max_value, tcp_source_address, node_namespace)

    def set_tags(self, tags:list):
        """
        Sets new values for a defined list of tags, 
        in thread-safe mechanism.
        
        **Parameters:**
        
        * **tags** (list): List of tag name, unit, data type, description, min and max value

        ```python
        >>> tags = [
                ("TAG1", 'ºC', 'float', 'Inlet temperature', 0.0, 100.0),
                ("TAG2", 'kPa', 'float', 'Inlet pressure', 100.0),
                ("TAG3", 'm3/s', 'float', 'Inlet flow')
            ]
        >>> tag_engine.set_tags(tags)
        ```
        """
        for tag_attrs in tags:

            if len(tag_attrs) >= 3:

                self.set_tag(*tag_attrs)

    def set_group(self, group:str, *tags):
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

    def delete_tag(self, name:str)->dict:
        r"""
        Deletes tag from database and tags repository by tag name

        **Parameters**

        * **name** (str): Tag name to delete

        **Returns**

        * **msg** (dict) Request message

        Message structure:

        ```python
        msg = {
            'message': 'Request message'
        }
        ```
        """

        if self.tag_defined(name):

            self._cvt.delete_tag(name)

            message = f"You deleted {name} tag successfully"

        else:

            message = f"{id} is not into database"

        return {
            'message': message
        }

    def get_group(self, group:str)->list:
        """
        Returns the tag list of the a defined group.
        
        **Parameters:**
        
        * **group** (str): Group name.

        **Returns**

        * **tag_names** (list) Tag names binded to a group

        ```python
        >>> tag_engine.get_group('Temperatures')
        ['TAG1', 'TAG2']
        >>> tag_engine.get_group('Pressures')
        ['TAG3', 'TAG4']
        ```
        """
        return self._groups[group]

    def get_groups(self)->list:
        """
        Returns a list of the group names defined.
        """

        return list(self._groups.keys())

    def get_tags(self)->list:
        """
        Returns a list of the tag names defined.
        """

        return self._cvt.get_tags()

    def write_tag(self, name:str, value:float)->dict:
        """
        Writes a new value for a defined tag, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag's name.
        * **value** (float, int, bool, str):  Tag's value ("int", "float", "bool", "str")

        **Returns**

        * **msg** (dict): Message for write request

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

    def read_tag(self, name:str, unit:str=None)->float:
        """
        Returns a tag value defined by name, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag name.

        **Returns**

        * **value** (float) Tag's value

        ```python
        >>> tag_engine.read_tag('TAG1')
        50.53
        ```
        """

        _query = dict()
        _query["action"] = "get_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name
        _query["parameters"]["unit"] = unit

        self.request(_query)
        result = self.response()

        if result["result"]:
            
            return result["response"]

    def attach(self, name:str, observer):
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

    def detach(self, name:str, observer):
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

    def read_data_type(self, name:str)->str:
        """
        Returns the tag's data type, in thread-safe mechanism.
        
        **Parameters:**

        * **name** (str): Tag's name.

        **Returns**

        * **data_type** (str) Tag's data type
        """

        _query = dict()
        _query["action"] = "get_data_type"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            
            return result["response"]

    def read_unit(self, name:str)->str:
        """
        Returns the tag's unit, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **unit** (str): Tag's unit.
        """

        _query = dict()
        _query["action"] = "get_unit"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            
            return result["response"]

    def read_description(self, name:str)->str:
        """
        Returns the tag's description, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **description** (str): Tag's description.
        """

        _query = dict()
        _query["action"] = "get_description"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_min_value(self, name:str)->float:
        """
        Returns the tag's min value, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **min_value** (float): Tag's min value.
        """

        _query = dict()
        _query["action"] = "get_min_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_max_value(self, name:str)->float:
        """
        Returns the tag's max value, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **max_value** (float): Tag's max value.
        """

        _query = dict()
        _query["action"] = "get_max_value"

        _query["parameters"] = dict()
        _query["parameters"]["name"] = name

        self.request(_query)
        result = self.response()

        if result["result"]:
            return result["response"]

    def read_attributes(self, name:str)->dict:
        """
        Returns all tag's attributes, in thread-safe mechanism.
        
        **Parameters:**
        
        * **name** (str): Tag name.

        **Returns**

        * **attrs** (dict) Tag's attributes

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
            'max_value': 100.0,
            'tcp_source_address': '',
            'node_namespace': ''
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

    def request(self, query:dict):
        r"""
        It does the request to the tags repository according query's structure, in a thread-safe mechanism

        **Parameters**

        * **query** (dict): Query to tags repository

        ## Query Structure

        ```python
        query = {
            "action": (str)
            "parameters": (dict)
        }
        ```
        ## Valid actions in query

        * set_tag
        * get_tags
        * get_value
        * get_data_type
        * get_unit
        * get_description
        * get_min_value
        * get_max_value
        * get_attributes
        * set_value
        * attach
        * detach

        ## Parameters strcuture in query

        ```python
        parameters = {
            "name": (str) tag name to do request
            "unit": (str)[Optional] Unit to get value
            "value": (float)[Optional] If you use *set_value* function, you must pass this parameter
            "observer": (TagObserver)[Optional] If you use *attach* and *detach* function, you must pass this parameter
        }
        ```

        """
        self._request_lock.acquire()
        parameters = query["parameters"]
        name = parameters["name"]
        action = query["action"]
        error_msg = f"Error in CVTEngine with action: {action}"

        try:

            if action == "set_tag":
                data_type = parameters["data_type"]
                resp = self._cvt.set_tag(name, data_type)
            
            elif action == "get_tags":
                resp = self._cvt.get_tags()

            elif action == "get_value":
                unit = parameters["unit"]
                resp = self._cvt.get_value(name, unit=unit)

            elif action == "get_data_type":
                resp = self._cvt.get_data_type(name)

            elif action == "get_unit":
                resp = self._cvt.get_unit(name)

            elif action == "get_description":
                resp = self._cvt.get_description(name)

            elif action == "get_min_value":
                resp = self._cvt.get_min_value(name)

            elif action == "get_max_value":
                resp = self._cvt.get_max_value(name)

            elif action == "get_attributes":
                resp = self._cvt.get_attributes(name)

            elif action == "set_value":
                value = parameters["value"]
                resp = self._cvt.set_value(name, value)

            elif action in ("attach", "detach"):
                observer = parameters["observer"]
                if action == "attach":
                    resp = self._cvt.attach_observer(name, observer)
                else:
                    resp = self._cvt.detach_observer(name, observer)

            self.__true_response(resp)

        except Exception as e:
            self.__log_error(e, error_msg)

        self._response_lock.release()

    def __log_error(self, e:Exception, msg:str):
        r"""
        Documentation here
        """
        log_detailed(e, msg)
        self._response = {
            "result": False,
            "response": None
        }

    def __true_response(self, resp):
        r"""
        Documentation here
        """
        self._response = {
            "result": True,
            "response": resp
        }

    def response(self)->dict:
        r"""
        Handles the python GIL to emit the request's response in a thread-safe mechanism.
        """
        self._response_lock.acquire()

        result = self._response

        self._request_lock.release()

        return result

    def serialize_tag(self, id:int)->dict:
        r"""
        Serialize a Tag Object in a jsonable object.

        **Parameters**

        * **id** (id) Tag name to serialize Tag Object

        **Returns**

        * **tag** (dict): Tag attributes in a jsonable object
        """
        attrs = self.read_attributes(id)

        try:
            result = attrs
        except:
            result = {
                'tag_name': id
            }

        return result

    def serialize(self)->list:
        r"""
        Serializes all tag's repository in a jsonable object.

        **Returns**

        * **cvt** (list): Tag's repository in a jsonable object.
        """
        result = list()

        tags = self.get_tags()

        for _tag in tags:

            record = self.serialize_tag(_tag)

            result.append(record)

        return result

    def serialize_group(self, name:str)->list:
        r"""
        Serializes all groups of the tag's repository in a jsonable object.

        **Returns**

        * **groups** (list): Groups of the tag's repository in a jsonable object.
        """
        result = list()

        tags = self.get_group(name)

        for _tag in tags:

            record = self.serialize_tag(_tag)

            result.append(record)

        return result

    def add_conversions(self, conversions_path:str):
        r"""
        Add new custom conversion factores between tag's units.

        **Parameters**

        * **conversions_path** (str) Url where the json file configuration for conversion factors is.
        """
        self._cvt.unit_converter.add_conversions(conversions_path)

    def add_variables(self, variables_path:str):
        r"""
        Add new variables and units.

        **Parameters**

        * **variables_path** (str) Url where the json file configuration for variables and units is.
        """
        try:
            f = open(variables_path)
            variables = json.load(f)

            for variable, units in variables.items():

                Variables.create(name=variable)
                
                for name, unit in units:

                    Units.create(name=name, unit=unit, variable=variable)

        except Exception as _err:

            message = "Error in Adding Variables and Units in CVT"
            log_detailed(_err, message)

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