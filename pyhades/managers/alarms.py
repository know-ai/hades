# -*- coding: utf-8 -*-
"""pyhades/managers/alarms.py
This module implements Alarm Manager.
"""
from datetime import datetime
import queue
from ..tags import CVTEngine, TagObserver
from ..dbmodels import AlarmLogging as AlarmModel
from ..dbmodels import AlarmsDB
from ..alarms import AlarmState
from ..alarms.alarms import Alarm


class AlarmManager:
    r"""
    This class implements all definitions for the Alarm Management System
    """

    def __init__(self):

        self._alarms = dict()
        self._tag_queue = queue.Queue()

    def get_queue(self)->queue.Queue:
        r"""
        Documentation here
        """
        return self._tag_queue
    
    def append_alarm(self, alarm:Alarm):
        r"""
        Append alarm to the Alarm Manager

        **Paramters**

        * **alarm**: (Alarm Object)

        **Returns**

        * **None**
        """
        self._alarms[f'{alarm._id}'] = alarm

    def update_alarm(self, id:int, **kwargs)->dict:
        r"""
        Updates alarm attributes

        **Parameters**

        * **id** (int).
        * **name** (str)[Optional]:
        * **tag** (str)[Optional]:
        * **description** (str)[Optional]:
        * **alarm_type** (str)[Optional]:
        * **trigger** (float)[Optional]:

        **Returns**

        * **alarm** (dict) Alarm Object jsonable
        """
        alarm = self._alarms[str(id)]
        alarm = alarm.update_alarm_definition(**kwargs)
        self._alarms[str(id)] = alarm
        return alarm.serialize()

    def delete_alarm(self, id:int):
        r"""
        Removes alarm

        **Paramters**

        * **id** (int): Alarm ID
        """
        alarm = AlarmsDB.read(id)
        
        if alarm:

            AlarmsDB.delete(id)    
            self._alarms.pop(str(id))

    def load_alarms_from_db(self):
        r"""
        Load alarms into alarm manager from database
        """
        manager_alarms = [alarm.name for id, alarm in self.get_alarms().items()]
        db_alarms = AlarmsDB.read_all()

        for db_alarm in db_alarms:

            if db_alarm['name'] not in manager_alarms:
                
                db_alarm.pop('id')
                alarm_trigger = {
                    'value': db_alarm.pop('trigger'),
                    '_type': db_alarm.pop('alarm_type')
                }
                alarm = Alarm(**db_alarm, load=True)
                alarm.set_trigger(**alarm_trigger)
                    
                self.append_alarm(alarm)

    def get_alarm(self, id:int)->Alarm:
        r"""
        Gets alarm from the Alarm Manager by id

        **Paramters**

        * **id**: (int) Alarm ID

        **Returns**

        * **alarm** (Alarm Object)
        """
        
        if str(id) in self._alarms.keys():

            return self._alarms[str(id)]
    
    def get_alarm_by_name(self, name:str)->Alarm:
        r"""
        Gets alarm from the Alarm Manager by name

        **Paramters**

        * **name**: (str) Alarm name

        **Returns**

        * **alarm** (Alarm Object)
        """
        for id, alarm in self._alarms.items():

            if name == alarm.name:

                return self._alarms[str(id)]
        
    def get_alarms_by_tag(self, tag:str)->dict:
        r"""
        Gets all alarms associated to some tag

        **Parameters**

        * **tag**: (str) tag name binded to alarm

        **Returns**

        * **alarm** (dict) of alarm objects
        """
        alarms = dict()
        for id, alarm in self._alarms.items():
            
            if tag == alarm.tag:
                
                alarms[id] = alarm

        return alarms

    def get_alarm_by_tag(self, tag:str)->dict:
        r"""
        Gets alarm associated to some tag

        **Parameters**

        * **tag**: (str) tag name binded to alarm

        **Returns**

        * **alarm** (list) of alarm objects
        """
        for id, alarm in self._alarms.items():
            
            if tag == alarm.tag:
                
                return {
                    id: alarm
                }

    def get_alarms(self)->dict:
        r"""
        Gets all alarms

        **Returns**

        * **alarms**: (dict) Alarm objects
        """
        return self._alarms

    def get_tag_alarms(self)->list:
        r"""
        Gets all tag alarms defined

        **Returns**

        * **tags_alarms**: (list) alarm tags
        """
        result = [_alarm.tag_alarm for id, _alarm in self.get_alarms().items()]

        return result

    def tags(self)->list:
        r"""
        Gets all tags variables binded into alarms

        **Returns**

        * **tags**: (list)
        """
        result = set([_alarm.tag for id, _alarm in self.get_alarms().items()])

        return list(result)

    def summary(self)->dict:
        r"""
        Summarizes all Alarm Manager

        **Returns**

        * **summary**: (dict)
        """
        result = dict()
        alarms = [_alarm.name for id, _alarm in self.get_alarms().items()]
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

        for id, _alarm in self._alarms.items():

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

        for id, _alarm in self._alarms.items():

            if _alarm.state == AlarmState.SHLVD:

                _now = datetime.now()
                
                if _alarm._shelved_until:

                    if _now >= _alarm._shelved_until:
                        
                        AlarmModel.create(
                            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            name=_alarm.name,
                            state=_alarm.state.state,
                            priority=_alarm._priority,
                            value=_alarm._value
                        )
                        
                        _alarm.unshelve()
                        continue

                    continue

                continue

            if tag == _alarm.tag:

                _alarm.update(value)
