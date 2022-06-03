from time import time
from .core import BaseModel
from peewee import DateTimeField, TextField, IntegerField, FloatField, CharField, ForeignKeyField
from datetime import datetime
from .tags import Tags

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class AlarmsType(BaseModel):

    name = CharField(unique=True)                       # high-high , high , bool , low , low-low
    trigger = FloatField()

    @classmethod
    def create(cls, name:str, trigger)-> dict:
        r"""
        You can use Model.create() to create a new model instance. This method accepts keyword arguments, where the keys correspond 
        to the names of the model's fields. A new instance is returned and a row is added to the table.

        ```python
        >>> AlarmsType.create(name='High-High')
        {
            'message': (str)
            'data': (dict) {
                'name': 'high-high'
            }
        }
        ```
        
        This will INSERT a new row into the database. The primary key will automatically be retrieved and stored on the model instance.

        **Parameters**

        * **name:** (str), Industrial protocol name

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (dict) row serialized}

        """
        result = dict()
        data = dict()
        name = name.lower()

        if not cls.name_exist(name):

            query = cls(name=name, trigger=trigger)
            query.save()
            
            message = f"Alarm type {name} created successfully"
            data.update(query.serialize())

            result.update(
                {
                    'message': message, 
                    'data': data
                }
            )
            return result

        message = f"Alarm type {name} is already into database"
        result.update(
            {
                'message': message, 
                'data': data
            }
        )
        return result

    @classmethod
    def read_by_name(cls, name:str)->bool:
        r"""
        Get instance by its a name

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name)
        
        if query is not None:

            return query.serialize()
        
        return None

    @classmethod
    def name_exist(cls, name:str)->bool:
        r"""
        Verify is a name exist into database

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name)
        
        if query is not None:

            return True
        
        return False

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """
        trigger = self.trigger
        if self.name.lower()=='bool':

            trigger = bool(trigger)

        return {
            "id": self.id,
            "name": self.name,
            "trigger": trigger
        }


class AlarmsDB(BaseModel):

    name = CharField(unique=True)
    tag = ForeignKeyField(Tags, backref='alarms', on_delete='CASCADE')
    desc = CharField()
    alarm_type = ForeignKeyField(AlarmsType, backref='alarms', on_delete='CASCADE')

    @classmethod
    def create(cls, name:str, tag:str, desc:str, alarm_type:str, trigger:float)-> dict:
        r"""
        You can use Model.create() to create a new model instance. This method accepts keyword arguments, where the keys correspond 
        to the names of the model's fields. A new instance is returned and a row is added to the table.

        ```python
        >>> AlarmsDB.create(name='alarm_PT_01_H', tag='PT-01', desc='Inlet Pressure Alarm', alarm_type='High-High', trigger=250.0)
        {
            'message': (str)
            'data': (dict) {
                'id': 1,
                'name': 'alarm_PT_01_H',
                'tag': 'PT-01',
                'desc': 'Inlet Pressure Alarm',
                'alarm_type': 'high-high',
                'trigger': 250.0
            }
        }
        ```
        
        This will INSERT a new row into the database. The primary key will automatically be retrieved and stored on the model instance.

        **Parameters**

        * **name:** (str), Industrial protocol name

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (dict) row serialized}

        """
        result = dict()
        data = dict()
        name = name.lower()

        if not cls.name_exist(name):

            query = cls(name=name, trigger=trigger)
            query.save()
            
            message = f"Alarm type {name} created successfully"
            data.update(query.serialize())

            result.update(
                {
                    'message': message, 
                    'data': data
                }
            )
            return result

        message = f"Alarm type {name} is already into database"
        result.update(
            {
                'message': message, 
                'data': data
            }
        )
        return result

    @classmethod
    def read_by_name(cls, name:str)->bool:
        r"""
        Get instance by its a name

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name)
        
        if query is not None:

            return query.serialize()
        
        return None

    @classmethod
    def name_exist(cls, name:str)->bool:
        r"""
        Verify is a name exist into database

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name)
        
        if query is not None:

            return True
        
        return False

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """
        trigger = self.trigger
        if self.name.lower()=='bool':

            trigger = bool(trigger)

        return {
            "id": self.id,
            "name": self.name,
            "trigger": trigger
        }



class AlarmsLogging(BaseModel):
    
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


class AlarmsSummary(BaseModel):
    
    name = TextField()
    state = TextField()
    alarm_time = DateTimeField()
    ack_time = DateTimeField(null=True)
    description = TextField()
    classification = TextField()
    priority = IntegerField(default=0)