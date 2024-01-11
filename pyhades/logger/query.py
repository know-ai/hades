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
    
    def get_oldest_record(self):
        r"""
        Documentation here
        """
        cursor = self._logger.get_db().cursor()
        query = f"""
SELECT * FROM tagvalue
ORDER BY id ASC LIMIT 1
        """
        cursor.execute(query)
        record_id, tag_id, tag_value, timestamp = cursor.fetchall()[0]
        return record_id, tag_id, tag_value, timestamp

    def get_current_record(self):
        r"""
        Documentation here
        """
        cursor = self._logger.get_db().cursor()
        query = f"""
SELECT * FROM tagvalue
ORDER BY id DESC LIMIT 1
        """
        cursor.execute(query)
        record_id, tag_id, tag_value, timestamp = cursor.fetchall()[0]
        return record_id, tag_id, tag_value, timestamp
    
    def query_trend_modified(self, start, stop, *tags):
        r"""
        Documentation here
        """
        _, _, _, current_record_timestamp = self.get_current_record()
        _, _, _, oldest_record_timestamp = self.get_oldest_record()
        start = datetime.strptime(start, DATETIME_FORMAT)
        if start < oldest_record_timestamp:
            start = oldest_record_timestamp
        stop = datetime.strptime(stop, DATETIME_FORMAT)
        if stop > current_record_timestamp:
            stop = current_record_timestamp
        seconds = (stop-start).total_seconds()
        inner_list = [[] for _ in range(len(tags))]
        outer_query = ""
        for tag in tags:
            tag_id = self.tag_engine.serialize_tag_by_name(tag)["id"]
            outer_query += f'AVG("value") FILTER (WHERE tag_id = {tag_id}) as VAR{tag_id},'
        
        outer_query = outer_query[:-1]
        interval = self.tag_engine._config['modules']['daq']['interval']
        points_to_get = seconds / interval
        if points_to_get < 5000:
            truncate_to = "milliseconds"
        elif points_to_get >= 5000 and points_to_get < 10000:
            truncate_to = "seconds"
        elif points_to_get >= 10000 and points_to_get < 300000:
            truncate_to = "minutes"
        elif points_to_get >= 300000 and points_to_get < 18000000:
            truncate_to = "hours"
        else:
            truncate_to = "days"

        result = {tag: {
            'values': list(),
            'unit': self.tag_engine.get_unit(tag)
        } for tag in tags}
        cursor = self._logger.get_db().cursor()
        query = f"""
SELECT
    ts,
    {outer_query}
FROM (
  SELECT
      date_trunc('{truncate_to}', timestamp) as ts,
      tag_id,
      value
  FROM tagvalue
  WHERE timestamp BETWEEN '{start}' AND '{stop}' 
  ORDER BY ts) as tv
GROUP BY ts
ORDER BY ts;
        """
        cursor.execute(query)
        query_result = cursor.fetchall()
        for timestamp, *data in query_result:
            
            for i, value in enumerate(data):
                
                inner_list[i].append(
                    {
                        "x": timestamp.strftime(DATETIME_FORMAT),
                        "y": value
                    }
                )
        for i, element in enumerate(inner_list):

            result[tags[i]]['values'] = element

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

    def query_values(self, stop, *tags):
        r"""
        Documentation here
        """        
        stop = datetime.strptime(stop, DATETIME_FORMAT)
        result = dict()

        for tag in tags:

            try:

                trend = Tags.select().where(Tags.name==tag).get()
                value = trend.values.select().where(TagValue.timestamp < stop).order_by(TagValue.timestamp.desc()).limit(1)
                result[tag] = {
                    'value': value[0].value if value else None,
                    'unit': self.tag_engine.get_unit(tag)
                }
            
            except:

                result[tag] = {
                    'value': None,
                    'unit': ""
                }

        return result