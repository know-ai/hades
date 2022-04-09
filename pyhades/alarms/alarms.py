# -*- coding: utf-8 -*-
"""pyhades/alarms.py

This module implements all Alarms class definitions and Alarm Handlers.
"""
from datetime import datetime, timedelta
from ..tags import CVTEngine
from ..dbmodels import Alarm as AlarmModel
from ..logger import DataLoggerEngine
from .states import AlarmState, Status
from .trigger import Trigger, TriggerType


class Alarm:

    tag_engine = CVTEngine()
    logger_engine = DataLoggerEngine()

    def __init__(self, name:str, tag:str, description:str):

        self._name = name
        self._tag = tag
        self._description = description
        self._value = False
        self._message = None
        self._state = AlarmState.NORM
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

    def get_trigger(self):
        r"""
        Documentation here
        """

        return self._trigger

    def set_trigger(self, value, _type:str):

        self._trigger.value = value
        self._trigger.type = _type

    @property
    def tag_alarm(self):
        r"""
        Documentation here
        """

        return self._tag_alarm

    @tag_alarm.setter
    def tag_alarm(self, tag):

        self._tag_alarm = tag

    def write_tag_alarm(self, value):

        if self._tag_alarm:

            self.tag_engine.write_tag(self._tag, value)
    
    @property
    def name(self):

        return self._name

    @property
    def tag(self):

        return self._tag

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def state(self):
        r"""
        Documentation here
        """
        return self._state

    @state.setter
    def state(self, _state):

        self._state = _state
        AlarmModel.create(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            name=self.name,
            state=self.state.state,
            description=self.description,
            priority=self._priority,
            value=self._value
        )

    def trigger_alarm(self):
        r"""
        Documentation here
        """
        if not self.enabled and self.state.acknowledge_status==Status.NA.value:

            return
       
        self._timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.state = AlarmState.UNACK

    @property
    def enabled(self):

        return self._enabled

    def enable(self, value:bool):

        if isinstance(value, bool):

            self._enable = value

    def acknowledge(self):

        if not self.enabled:

            return

        if self.state == AlarmState.UNACK:

            self.state = AlarmState.ACKED
        
        if self.state == AlarmState.RTNUN:
            
            self.state = AlarmState.NORM

        self._acknowledged_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def silence(self):

        if not self._enabled:

            return

        self._silence = True

    def sound(self):

        if not self._enabled:

            return
        
        self._silence = False
        
    def reset(self):

        self._enabled = True
        self._timestamp = None
        self._acknowledged_timestamp = None
        self._silence = False
        self.state = AlarmState.NORM

    def shelve(
        self, 
        **options):
        r"""
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

    def unshelve(self):
        r"""
        Documentation here
        """
        self._shelved_time = None
        self._shelved_until = None
        self.state = AlarmState.NORM

    def supress_by_design(self):
        r"""
        Documentation here
        """
        self.state = AlarmState.DSUPR

    def unsupress_by_design(self):
        r"""
        Documentation here
        """
        self.state = AlarmState.NORM

    def out_of_service(self):
        r"""
        Documentation here
        """
        self.state = AlarmState.OOSRV
    
    def in_service(self):

        self.state = AlarmState.NORM

    def update(self, value):

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
        Documentation here
        """
        return {
            "timestamp": self._timestamp,
            "name": self.name,
            "tag": self.tag,
            "tag_alarm": self.tag_alarm,
            "state": self.state.state,
            "enabled": self.enabled,
            "process": self.state.process_condition,
            "triggered": self.state.is_triggered,
            "trigger_value": self._trigger.value,
            "acknowledged": self.state.is_acknowledged(),
            "acknowledged_timestamp": self._acknowledged_timestamp,
            "value": self._value,
            "type": self._trigger.type,
            "audible": self.state.audible,
            "description": self.description
            
        }
