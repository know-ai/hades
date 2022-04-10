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

    def __init__(self):

        self._alarms = list()
        self._tag_queue = queue.Queue()

    def get_queue(self):

        return self._tag_queue
    
    def append_alarm(self, alarm):

        self._alarms.append(alarm)

    def get_alarm(self, name):

        for _alarm in self._alarms:
            if name == _alarm.name:
                return _alarm

        return

    def get_alarms_by_tag(self, tag):
        r"""
        Gets all alarms associated to some tag
        """
        alarms = list()
        for alarm in self._alarms:
            
            if tag == alarm.tag:
                
                alarms.append(alarm)

        return alarms

    def get_alarms(self):

        return self._alarms

    def get_tag_alarms(self):

        result = [_alarm.tag_alarm for _alarm in self.get_alarms()]

        return result

    def tags(self):

        result = set([_alarm.tag for _alarm in self.get_alarms()])

        return list(result)

    def summary(self):

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

    def execute(self, tag):

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
