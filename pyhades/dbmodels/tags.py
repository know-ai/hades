from peewee import CharField, DateTimeField, FloatField, ForeignKeyField
from .core import BaseModel
from datetime import datetime

class TagTrend(BaseModel):

    name = CharField(unique=True)
    start = DateTimeField()
    period = FloatField()

    @classmethod
    def create(cls, name, start, period):
        
        if not cls.name_exist(name):
            trend = cls(name=name, start=start, period=period)
            trend.save()

            return trend

    @classmethod
    def read_by_name(cls, name):
        trend = cls.select().where(cls.name == name).get()
        return trend

    @classmethod
    def update(cls):

        pass

    @classmethod
    def delete(cls):

        pass

    @classmethod
    def name_exist(cls, name):
        r"""
        Documentation here
        """
        tag = cls.get_or_none(name=name)
        if tag is not None:

            return True
        
        return False


class TagValue(BaseModel):

    tag = ForeignKeyField(TagTrend, backref='values')
    value = FloatField()
    timestamp = DateTimeField(default=datetime.now)
