from time import time
from .core import BaseModel
from peewee import DateTimeField, TextField, IntegerField, CharField, FloatField
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class Alarm(BaseModel):
    
    timestamp = DateTimeField(default=datetime.now)
    name = TextField()
    state = TextField()
    description = TextField()
    priority = IntegerField()
    value = FloatField()

    @classmethod
    def create(cls, timestamp, name, state, description, priority, value):
        alarm = cls(timestamp=timestamp, name=name, state=state, description=description, priority=priority, value=value)
        alarm.save()

    @classmethod
    def read(cls, lasts:int=1):

        alarms = cls.select().order_by(cls.id.desc())[0:lasts]
    
        return alarms

    @classmethod
    def update(cls):

        pass

    @classmethod
    def delete(cls):

        pass

    def serialize(self):
        r"""
        Documentation here
        """
        result = {
            "timestamp": self.timestamp.strftime(DATETIME_FORMAT),
            "name": self.name,
            "state": self.state,
            "description": self.description,
            "priority": self.priority,
            "value": self.value
        }

        return result


class AlarmSummary(BaseModel):
    
    name = TextField()
    state = TextField()
    alarm_time = DateTimeField()
    ack_time = DateTimeField(null=True)
    description = TextField()
    classification = TextField()
    priority = IntegerField(default=0)