# -*- coding: utf-8 -*-
"""pyhades/dbmodels.py

This module implements classes for
modelling the trending process.
"""
from datetime import datetime

from peewee import Proxy, Model, CharField, DateTimeField, FloatField, ForeignKeyField

proxy = Proxy()

SQLITE = 'sqlite'
MYSQL = 'mysql'
POSTGRESQL = 'postgresql'


class BaseModel(Model):
    class Meta:
        database = proxy


class TagTrend(BaseModel):

    name = CharField()
    start = DateTimeField()
    period = FloatField()


class TagValue(BaseModel):

    tag = ForeignKeyField(TagTrend, backref='values')
    value = FloatField()
    timestamp = DateTimeField(default=datetime.now)