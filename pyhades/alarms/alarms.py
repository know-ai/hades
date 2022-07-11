# -*- coding: utf-8 -*-
"""pyhades/alarms.py

This module implements all Alarms class definitions and Alarm Handlers.
"""
from datetime import datetime, timedelta
from ..tags import CVTEngine
from ..dbmodels import AlarmLogging as AlarmModel
from ..logger import DataLoggerEngine
from .states import AlarmState, Status
from .trigger import Trigger, TriggerType
from ..dbmodels import AlarmsDB


class Alarm:
    r"""
    This class implements all definitions for Alarm object
    """

    tag_engine = CVTEngine()
    logger_engine = DataLoggerEngine()

    def __init__(self, name:str, tag:str, description:str):

        self._name = name
        self._tag = tag
        self._description = description
        self._value = False
        self._message = None
        self._state = AlarmState.NORM
        self._mnemonic = AlarmState.NORM.mnemonic
        self._trigger = Trigger()
        self._tag_alarm = None
        self._enabled = True
        self._deadband = None
        self._priority = 0
        self._on_delay = None
        self._off_delay = None
        self._timestamp = None
        self._acknowledged_timestamp = None
        self._shelved_time = None
        self._shelved_options_time = {
            'days': 0,
            'seconds': 0,
            'microseconds': 0,
            'milliseconds': 0,
            'minutes': 0,
            'hours': 0,
            'weeks': 0
        }
        self._shelved_until = None
        self.__default_operations()
        AlarmsDB.create(name=name, tag=tag, desc=description)

    def __default_operations(self):
        r"""
        Documentation here
        """
        self._operations = {
            'acknowledge': 'not active',
            'enable': 'not active',
            'disable': 'active',
            'silence': 'not active',
            'shelve': 'active',
            'suppress by design': 'active',
            'unsuppressed': 'not active',
            'out of service': 'active',
            'return to service': 'not active',
            'reset': 'active'
        }

    def get_operations(self):
        r"""
        Documentation here
        """
        return self._operations

    def get_trigger(self):
        r"""
        Gets Trigger object for alarm
        """

        return self._trigger

    def set_trigger(self, value, _type:str):
        r"""
        Sets Trigger object for alarm

        **Parameters**

        * **value**: (int - float - bool) Value at which the alarm is triggered
        * **_type**: (str) ["HIGH-HIGH" - "HIGH" - "LOW" - "LOW-LOW" - "BOOL"] Alarm type
        """
        self._trigger.value = value
        self._trigger.type = _type
        alarm = AlarmsDB.read_by_name(self.name)
        alarm.set_trigger(alarm_type=_type, trigger=float(value))

    @property
    def value(self):
        r"""
        Property Sets and Gets current value of the tag that the alarm monitors
        """
        return self._value

    @value.setter
    def value(self, value):

        self._value = value

    @property
    def tag_alarm(self):
        r"""
        Property (str) Sets and Gets tag of the alarm
        """

        return self._tag_alarm

    @tag_alarm.setter
    def tag_alarm(self, tag):

        self._tag_alarm = tag

    def write_tag_alarm(self, value):
        r"""
        Documentation for write_tag_alarm
        """
        if self._tag_alarm:

            self.tag_engine.write_tag(self._tag, value)
    
    @property
    def name(self):
        r"""
        Property (str) Sets and Gets Alarm name
        """
        return self._name

    @property
    def tag(self):
        r"""
        Property (str) Sets and Gets tag of the CVT that alarm monitors
        """
        return self._tag

    @property
    def description(self):
        r"""
        Property (str) Sets and Gets alarm description
        """
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def state(self):
        r"""
        Property (AlarmState Object) Sets and Gets Alarm state
        """
        return self._state

    @state.setter
    def state(self, _state):

        self._state = _state
        AlarmModel.create(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            name=self.name,
            state=self.state.state,
            priority=self._priority,
            value=self._value
        )

    def trigger_alarm(self):
        r"""
        Trigger alarm in Unacknowledge state if the alarm is enabled
        """
        if not self.enabled and self.state.acknowledge_status==Status.NA.value:

            return
       
        self._timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.state = AlarmState.UNACK
        self._operations['acknowledge'] = 'active'
        self._operations['shelve'] = 'not active'
        self._operations['suppress by design'] = 'not active'
        self._operations['out of service'] = 'not active'

    @property
    def enabled(self):
        r"""
        Property, check if alarm is enabled
        """
        return self._enabled

    def enable(self):
        r"""
        Enable or disable alarm according the parameter *value*

        **Parameters**

        * **value**: (bool) if *True* enable alarm, otherwise, disable it
        """

        self._enabled = True

        self._operations['disable'] = 'active'
        self._operations['enable'] = 'not active'

    def disable(self):
        r"""
        Enable or disable alarm according the parameter *value*

        **Parameters**

        * **value**: (bool) if *True* enable alarm, otherwise, disable it
        """

        self._enabled = False

        self._operations['disable'] = 'not active'
        self._operations['enable'] = 'active'

    def acknowledge(self):
        r"""
        Allows you to acknowledge alarm triggered
        """
        if not self.enabled:

            return

        if self.state == AlarmState.UNACK:

            self.state = AlarmState.ACKED
        
        if self.state == AlarmState.RTNUN:
            
            self.state = AlarmState.NORM

        self._acknowledged_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._operations['acknowledge'] = 'not active'

    def silence(self):
        r"""
        Documentation here for silence alarm
        """
        if not self._enabled:

            return

        self._silence = True
        self._operations['silence'] = 'not active'

    def sound(self):
        r"""
        Documentation here for sound alamr
        """
        if not self._enabled:

            return
        
        self._silence = False
        
    def reset(self):
        r"""
        Returns alarm to normal condition
        """
        self._enabled = True
        self._timestamp = None
        self._acknowledged_timestamp = None
        self._silence = False
        self.state = AlarmState.NORM
        self.__default_operations()

    def shelve(
        self, 
        **options):
        r"""
        Set alarm to Shelved state

        **Parameters**

        * **days:** (int)
        * **seconds:** (int)
        * **minutes:** (int)
        * **hours:** (int)
        * **weeks:** (int)
        """
        options_time = {key: options[key] if key in options else self._shelved_options_time[key] for key in self._shelved_options_time}
        
        if options_time!=self._shelved_options_time:
            
            self._shelved_time = datetime.now()
            self._shelved_until = self._shelved_time + timedelta(**options_time)
        
        self.state = AlarmState.SHLVD
        self._operations['shelve'] = 'not active'
        self._operations['suppress by design'] = 'not active'
        self._operations['out of service'] = 'not active'

    def unshelve(self):
        r"""
        Set Alarm to normal state after Shelved state
        """
        self._shelved_time = None
        self._shelved_until = None
        self.state = AlarmState.NORM
        self._operations['shelve'] = 'active'
        self._operations['suppress by design'] = 'active'
        self._operations['out of service'] = 'nactive'

    def suppress_by_design(self):
        r"""
        Suppress Alarm by design
        """
        self.state = AlarmState.DSUPR
        self._operations['shelve'] = 'not active'
        self._operations['suppress by design'] = 'not active'
        self._operations['out of service'] = 'not active'
        self._operations['unsuppress by design'] = 'active'

    def unsuppress_by_design(self):
        r"""
        Unsuppress alarm, return to normal state after suppress state
        """
        self.state = AlarmState.NORM
        self._operations['shelve'] = 'active'
        self._operations['suppress by design'] = 'active'
        self._operations['out of service'] = 'active'

    def out_of_service(self):
        r"""
        Remove alarm from service
        """
        self.state = AlarmState.OOSRV
        self._operations['shelve'] = 'not active'
        self._operations['suppress by design'] = 'not active'
        self._operations['out of service'] = 'not active'
        self._operations['return to service'] = 'active'
    
    def return_to_service(self):
        r"""
        Return alarm to normal condition after Out Of Service state
        """
        self.state = AlarmState.NORM
        self._operations['shelve'] = 'active'
        self._operations['suppress by design'] = 'active'
        self._operations['out of service'] = 'active'

    def update(self, value):
        r"""
        Update alarm state according the tag value that the alarm monitors and according its state

        **Parameters**

        * **value**: (int - float - bool) according alarm type, current tag value
        """
        if not self.enabled and self.state.acknowledge_status==Status.NA.value:

            return

        self._value = value

        _type = self._trigger.type

        if self.state in (AlarmState.NORM, AlarmState.RTNUN):

            if (_type == TriggerType.H) or (_type == TriggerType.HH):

                if value >= self._trigger.value:
                
                    self.trigger_alarm()

            elif (_type == TriggerType.L) or (_type == TriggerType.LL):
                
                if value <= self._trigger.value:
                
                    self.trigger_alarm()

            elif _type == TriggerType.B:
                
                if value == self._trigger.value:
                
                    self.trigger_alarm()

        elif self.state == AlarmState.UNACK:

            if (_type == TriggerType.H) or (_type == TriggerType.HH):
                
                if value < self._trigger.value:
                
                    self.state = AlarmState.RTNUN

            elif (_type == TriggerType.L) or (_type == TriggerType.LL):
                
                if value > self._trigger.value:
                
                    self.state = AlarmState.RTNUN

            elif _type == TriggerType.B:

                if value != self._trigger.value:
                
                    self.state = AlarmState.RTNUN

        elif self.state == AlarmState.ACKED:

            if (_type == TriggerType.H) or (_type == TriggerType.HH):
                
                if value < self._trigger.value:
                
                    self.state = AlarmState.NORM

            elif (_type == TriggerType.L) or (_type == TriggerType.LL):
                
                if value > self._trigger.value:
                
                    self.state = AlarmState.NORM

            elif _type == TriggerType.B:
                
                if value != self._trigger.value:
                
                    self.state = AlarmState.NORM

    def serialize(self):
        r"""
        Allows you to serialize alarm to a dict jsonable

        **Return**

        * **alarm_info**: (dict) A jsonable dictionary
        """
        return {
            "timestamp": self._timestamp,
            "name": self.name,
            "tag": self.tag,
            "tag_alarm": self.tag_alarm,
            "state": self.state.state,
            "mnemonic": self.state.mnemonic,
            "enabled": self.enabled,
            "process": self.state.process_condition,
            "triggered": self.state.is_triggered,
            "trigger_value": self._trigger.value,
            "acknowledged": self.state.is_acknowledged(),
            "acknowledged_timestamp": self._acknowledged_timestamp,
            "value": self._value,
            "type": self._trigger.type.value,
            "audible": self.state.audible,
            "description": self.description,
            "operations": self.get_operations()
            
        }
