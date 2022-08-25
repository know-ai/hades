# -*- coding: utf-8 -*-
"""pyhades/logger/datalogger.py

This module implements a database logger for the CVT instance, 
will create a time-serie for each tag in a short memory data base.
"""
from ..dbmodels import (
    Tags, 
    TagValue, 
    AlarmTypes, 
    AlarmPriorities, 
    AlarmStates, 
    Variables, 
    Units,
    DataTypes)

from ..alarms.trigger import TriggerType
import json, os
from ..src import get_directory
from ..alarms.states import AlarmState


class DataLogger:

    """Data Logger class.

    This class is intended to be an API for tags 
    settings and tags logged access.

    # Example
    
    ```python
    >>> from pyhades import DataLogger
    >>> _logger = DataLogger()
    ```
    """

    def __init__(self):

        self._db = None

    def set_db(self, db):

        self._db = db

    def get_db(self):
        
        return self._db

    def set_tag(
        self, 
        tag, 
        unit:str, 
        data_type:str, 
        description:str, 
        min_value:float=None, 
        max_value:float=None, 
        tcp_source_address:str=None, 
        node_namespace:str=None):

        Tags.create(
            name=tag, 
            unit=unit,
            data_type=data_type,
            description=description,
            min_value=min_value,
            max_value=max_value,
            tcp_source_address=tcp_source_address,
            node_namespace=node_namespace)

    def set_tags(self, tags):
        
        for tag in tags:

            self.set_tag(tag)
    
    def create_tables(self, tables):
        if not self._db:
            
            return
        
        self._db.create_tables(tables, safe=True)
        self.__init_default_alarms_schema()
        self.__init_default_variables_schema()
        self.__init_default_datatypes_schema()

    def __init_default_variables_schema(self):
        r"""
        Documentation here
        """
        filename = os.path.join(get_directory('src'), 'variables.json')
        f = open(filename)
        variables = json.load(f)

        for variable, units in variables.items():
            if not Variables.name_exist(variable):
                
                Variables.create(name=variable)
            
            for name, unit in units:
                
                if not Units.name_exist(name):

                    Units.create(name=name, unit=unit, variable=variable)

    def __init_default_datatypes_schema(self):
        r"""
        Documentation here
        """
        datatypes = [
            "float",
            "int",
            "bool",
            "str"
        ]
        for datatype in datatypes:

            DataTypes.create(name=datatype)

    def __init_default_alarms_schema(self):
        r"""
        Documentation here
        """
        ## Alarm Types
        for alarm_type in TriggerType:

            AlarmTypes.create(name=alarm_type.value)

        ## Alarm Priorities
        alarm_priorities = [
            (0, 'Not priority'),
            (1, 'Low low priority'),
            (2, 'Low priority'),
            (3, 'Normal priority'),
            (4, 'High priority'),
            (5, 'High High priority')
        ]
        for value, description in alarm_priorities:

            AlarmPriorities.create(value=value, description=description)

        ## Alarm States
        for alarm_state in AlarmState._states:
            name = alarm_state.state
            mnemonic = alarm_state.mnemonic
            condition = alarm_state.process_condition
            status = alarm_state.alarm_status
            AlarmStates.create(name=name, mnemonic=mnemonic, condition=condition, status=status)

    def drop_tables(self, tables):

        if not self._db:
            
            return

        self._db.drop_tables(tables, safe=True)

    def write_tag(self, tag, value):

        trend = Tags.read_by_name(tag)
        tag_value = TagValue.create(tag=trend, value=value)
        tag_value.save()

    def read_tag(self, tag):
        
        query = Tags.select().order_by(Tags.start)
        trend = query.where(Tags.name == tag).get()
        
        period = trend.period
        values = trend.values.select()
        
        result = dict()

        t0 = values[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')
        values = [value.value for value in values]

        result["t0"] = t0
        result["dt"] = period
        result["values"] = values
        
        return result
