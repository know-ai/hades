# -*- coding: utf-8 -*-
"""pyhades/managers/alarms.py
This module implements Alarm Manager.
"""
from datetime import datetime
import queue
from ..tags import CVTEngine, TagObserver
from ..dbmodels import Alarm as AlarmModel
from ..alarms import AlarmState


class AlarmManager:
    r"""
    This class implements all definitions for the Alarm Management System
    """

    def __init__(self):

        self._alarms = list()
        self._tag_queue = queue.Queue()

    def get_queue(self):
        r"""
        Documentation here
        """
        return self._tag_queue
    
    def append_alarm(self, alarm):
        r"""
        Append alarm to the Alarm Manager

        **Paramters**

        * **alarm**: (Alarm Object)

        **Returns** `None`
        """
        self._alarms.append(alarm)

    def get_alarm(self, name:str):
        r"""
        Gets alarm from the Alarm Manager by the alarm name

        **Paramters**

        * **name**: (str) Alarm name

        **Returns**

        * **alarm** (Alarm Object)
        """
        for _alarm in self._alarms:
            
            if name == _alarm.name:
                
                return _alarm

        return

    def get_alarms_by_tag(self, tag:str):
        r"""
        Gets all alarms associated to some tag

        **Parameters**

        * **tag**: (str) tag name defined in cvt associated to the alarm

        **Returns**

        * **alarm** (list) of alarm objects
        """
        alarms = list()
        for alarm in self._alarms:
            
            if tag == alarm.tag:
                
                alarms.append(alarm)

        return alarms

    def get_alarms(self):
        r"""
        Gets all alarms defined in the Alarm Manager

        **Returns**

        * **alarms**: (list) Alarm objects
        """
        return self._alarms

    def get_tag_alarms(self):
        r"""
        Gets all tag alarms defined

        **Returns**

        * **tags_alarms**: (list) alarm tags
        """
        result = [_alarm.tag_alarm for _alarm in self.get_alarms()]

        return result

    def tags(self):
        r"""
        Gets all tags variables subscribed into alarms

        **Returns**

        * **tags**: (list)
        """
        result = set([_alarm.tag for _alarm in self.get_alarms()])

        return list(result)

    def summary(self):
        r"""
        Summarizes all Alarm Manager

        **Returns**

        * **summary**: (dict)
        """
        result = dict()

        alarms = [_alarm.name for _alarm in self.get_alarms()]
        
        result["length"] = len(alarms)
        result["alarms"] = alarms
        result["alarm_tags"] = self.get_tag_alarms()
        result["tags"] = self.tags()

        return result

    def attach_all(self):

        _cvt = CVTEngine()

        def attach_observers(entity):

            _tag = entity.tag

            observer = TagObserver(self._tag_queue)
            query = dict()
            query["action"] = "attach"
            query["parameters"] = {
                "name": _tag,
                "observer": observer,
            }
            _cvt.request(query)
            _cvt.response()

        for _alarm in self._alarms:

            attach_observers(_alarm)

    def execute(self, tag:str):
        r"""
        Execute update state value of alarm if the value store in cvt for tag 
        reach alarm threshold values

        **Paramters**

        * **tag**: (str) Tag in CVT
        """
        _cvt = CVTEngine()
        value = _cvt.read_tag(tag)

        for _alarm in self._alarms:

            if _alarm.state == AlarmState.SHLVD:

                _now = datetime.now()
                
                if _alarm._shelved_until:

                    if _now >= _alarm._shelved_until:
                        
                        AlarmModel.create(
                            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            name=_alarm.name,
                            state=_alarm.state.state,
                            description=_alarm.description,
                            priority=_alarm._priority,
                            value=_alarm._value
                        )
                        
                        _alarm.unshelve()
                        continue

                    continue

                continue

            if tag == _alarm.tag:

                _alarm.update(value)

                break
