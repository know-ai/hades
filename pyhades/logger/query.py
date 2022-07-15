# -*- coding: utf-8 -*-
"""rackio/logger/query.py

This module implements a QueryLogger layer class,
to retrieve history, trends and waveforms from database.
"""

from datetime import datetime, timedelta

from .engine import DataLoggerEngine
from ..dbmodels import Tags, TagValue

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class QueryLogger:

    def __init__(self):

        self._logger = DataLoggerEngine()

    def get_values(self, tag):

        query = Tags.select().order_by(Tags.start.description())
        trend = query.where(Tags.name == tag).get()
        values = trend.values
        
        return values

    def get_period(self, tag):

        query = Tags.select().order_by(Tags.start.description())
        trend = query.where(Tags.name == tag).get()
        
        return float(trend.period)

    def get__value(self, tag):
        r"""
        Documentation here
        """
        return self.get_values()

    def get_start(self, tag):

        query = Tags.select().order_by(Tags.start.description())
        trend = query.where(Tags.name == tag).get()
        
        return trend.start

    def query_waveform(self, tag, start, stop):

        _query = Tags.select().order_by(Tags.start)
        trend = _query.where(Tags.name == tag).get()
        
        start = datetime.strptime(start, DATETIME_FORMAT)
        stop = datetime.strptime(stop, DATETIME_FORMAT)

        period = trend.period
        
        _query = trend.values.select().order_by(TagValue.timestamp.asc())
        values = _query.where((TagValue.timestamp > start) & (TagValue.timestamp < stop))
        
        result = dict()

        t0 = values[0].timestamp.strftime(DATETIME_FORMAT)

        result["t0"] = t0
        result["dt"] = period
        
        result["values"] = values

        return result

    def query_trend(self, tag, start, stop):

        _query = Tags.select().order_by(Tags.start)
        trend = _query.where(Tags.name == tag).get()
        
        start = datetime.strptime(start, DATETIME_FORMAT)
        stop = datetime.strptime(stop, DATETIME_FORMAT)
        
        _query = trend.values.select().order_by(TagValue.timestamp.asc())
        values = _query.where((TagValue.timestamp > start) & (TagValue.timestamp < stop))

        result = dict()

        values = [{"x": value.timestamp.strftime(DATETIME_FORMAT), "y": value.value} for value in values]
        result["values"] = values

        return result

    def query_last(self, tag, seconds=None, waveform=False):

        stop = datetime.now()
    
        if seconds==None:

            seconds = self.get_period(tag)

        start = stop - timedelta(seconds=seconds)
        stop = stop.strftime(DATETIME_FORMAT)
        start = start.strftime(DATETIME_FORMAT)

        if waveform:

            return self.query_waveform(tag, start, stop)

        return self.query_trend(tag, start, stop)


    def query_first(self, tag, seconds=None, waveform=False):

        tag_values = self.get_values(tag)
        start = tag_values[0].timestamp

        if seconds:
            
            stop = start + seconds

        else:

            stop = start + self.get_period(tag)

        start = start.strftime(DATETIME_FORMAT)
        stop = stop.strftime(DATETIME_FORMAT)
        if waveform:

            return self.query_waveform(tag, start, stop)
        
        return self.query_trend(tag, start, stop)

