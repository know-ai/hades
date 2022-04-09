from peewee import CharField, DateTimeField, FloatField, ForeignKeyField
from .core import BaseModel
from datetime import datetime

class TagTrend(BaseModel):

    name = CharField()
    start = DateTimeField()
    period = FloatField()

class TagValue(BaseModel):

    tag = ForeignKeyField(TagTrend, backref='values')
    value = FloatField()
    timestamp = DateTimeField(default=datetime.now)