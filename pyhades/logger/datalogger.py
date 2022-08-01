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
            # self.set_tag(tag, period)
    
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
        variables = {
            "Pressure": [
                ("pascal", "Pa"), 
                ("kilopascal", "kPa"),
                ("megapascal", "MPa"), 
                ("milimeter_of_mercury", "mmHg"), 
                ("pound_square_inch", "psi"), 
                ("atmospheres", "atm"), 
                ("bar", "bar"),
                ("inches_of_water", 'inH2O'),
                ("inches_of_mercury", "inHg"),
                ("centimeter_of_mercury", "cmHg"),
                ("foot_of_water", "ftH2O"),
                ("meters_of_water", "mH2O"),
                ("kilogram_force_centimeter_square", "kgf/cm2")
            ],
            "Temperature": [
                ("degree_celsius", "ªC"),
                ("degree_fahrenheit", "ªF"),
                ("degree_kelvin", "K"), 
                ("degree_rankine", "R")
            ],
            "Time": [
                ("milisecond", "ms"), 
                ("second", "s"), 
                ("minute", "min"), 
                ("hour", "h"), 
                ("day", "day")
            ],
            "MolarFlow": [
                ("kilomole_second", "kmole/s"), 
                ("kilomole_minute", "kmole/min"), 
                ("kilomole_hour", "kmole/h")
            ],
            "MassFlow": [
                ("kilogram_second", "kg/s"), 
                ("kilogram_minute", "kg/min"), 
                ("kilogram_hour", "kg/h"), 
                ("gram_second", "g/s"), 
                ("gram_minute", "g/min"), 
                ("gram_hour", "g/h")
            ],
            "VolumetricFlow": [
                ("liter_second", "l/s"), 
                ("liter_minute", "l/min"), 
                ("liter_hour", "l/h"), 
                ("meter_cube_second", "m3/s"), 
                ("meter_cube_minute", "m3/min"), 
                ("meter_cube_hour", "m3/h")
            ],
            "MassDensity": [
                ("kilogram_meter_cube", "kg/m3"),
                ("gram_mililiter", "g/ml"),
                ("pound_foot_cube", "lb/ft3"),
                ("pound_inch_cubre","lb/in3")
            ],
            "MolarDensity": [
                ("kilomole_meter_cube", "kmole/m3")
            ],
            "Speed": [
                ("meter_second", "m/s"), 
                ("kilometer_hour", "km/h"),
                ("meter_minute", "m/min"),
                ("foot_second", "ft/s"),
                ("foot_minute", "ft/min"),
                ("miles_hour", "miles/h")
            ],
            "Length": [
                ("milimeters", "mm"), 
                ("centimeters", "cm"), 
                ("meters","m"), 
                ("kilometers", "km"), 
                ("inches", "in"), 
                ("feet", "ft"),
                ("yards", "yd"),
                ("miles", "miles")
            ],
            "Undefined": [
                ("Adimensional", "Adim"), 
                ("not_defined", "")
            ]
        }

        ## Alarm Types
        for variable, units in variables.items():

            Variables.create(name=variable)
            
            for name, unit in units:

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
        ## Alarm Types
        for datatype in datatypes:

            DataTypes.create(name=datatype)

    def __init_default_alarms_schema(self):
        r"""
        Documentation here
        """
        # Init Default Databases

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
