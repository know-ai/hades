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
        from ..tags import CVTEngine
        self._logger = DataLoggerEngine()
        self.tag_engine = CVTEngine()

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

        trend = Tags.select().where(Tags.name == tag).order_by(Tags.start).get()
        start = datetime.strptime(start, DATETIME_FORMAT)
        stop = datetime.strptime(stop, DATETIME_FORMAT)
        period = trend.period
        values= trend.values.select().where((TagValue.timestamp > start) & (TagValue.timestamp < stop)).order_by(TagValue.timestamp.asc())
        result = dict()
        t0 = values[0].timestamp.strftime(DATETIME_FORMAT)
        result["t0"] = t0
        result["dt"] = period
        result["values"] = values

        return result

    def query_trend(self, tag, start, stop):

        trend = Tags.select().where(Tags.name == tag).order_by(Tags.start).get()
        start = datetime.strptime(start, DATETIME_FORMAT)
        stop = datetime.strptime(stop, DATETIME_FORMAT)
        values = trend.values.select().where((TagValue.timestamp > start) & (TagValue.timestamp < stop)).order_by(TagValue.timestamp.asc())
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


    def query_lasts(self, seconds=None, *tags):
        r"""
        Documentation here
        """
        stop = datetime.now()
    
        if seconds==None:

            seconds = self.get_period(tags[0])

        start = stop - timedelta(seconds=seconds)
        stop = stop.strftime(DATETIME_FORMAT)
        start = start.strftime(DATETIME_FORMAT)

        return self.query_trends(start, stop, *tags)

    def query_current(self, *tags):
        r"""
        Documentation here
        """
        result = dict()
        timestamp = datetime.now().strftime(DATETIME_FORMAT)[:-5]
        
        for tag in tags:
        
            trend = Tags.select().where(Tags.name==tag).order_by(Tags.start).get()
            if trend:
                value = trend.values.select().order_by(TagValue.timestamp.desc())
                if value:
                    value = value.get()
                    result[value.tag.name] = {"x": timestamp, "y": value.value}
        
        return result

    def query_trends(self, start, stop, *tags):
        r"""
        Documentation here
        """        
        start = datetime.strptime(start, DATETIME_FORMAT)
        stop = datetime.strptime(stop, DATETIME_FORMAT)
        result = {tag: {
            'values': list(),
            'unit': self.tag_engine.get_unit(tag)
        } for tag in tags}
        

        for tag in tags:

            trend = Tags.select().where(Tags.name==tag).get()
            
            values = trend.values.select().where((TagValue.timestamp > start) & (TagValue.timestamp < stop)).order_by(TagValue.timestamp.asc())

            for value in values:
                
                result[tag]['values'].append({"x": value.timestamp.strftime(DATETIME_FORMAT), "y": value.value})


        return result