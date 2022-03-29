# -*- coding: utf-8 -*-
"""pyhades/logger/datalogger.py

This module implements a database logger for the CVT instance, 
will create a time-serie for each tag in a short memory data base.
"""

from datetime import datetime

from ..dbmodels import TagTrend, TagValue


class DataLogger:

    """Data Logger class.

    This class is intended to be an API for tags 
    settings and tags logged access.

    # Example
    
    ```python
    >>> from pyhades import DataLogger
    >>> _logger = DataLogger()
    ```
    
    """

    def __init__(self):

        self._db = None
        self.tags_dbo = dict()

    def set_db(self, db):

        self._db = db

    def get_db(self):
        
        return self._db

    def set_tag(self, tag, period):

        now = datetime.now()
        trend = TagTrend(name=tag, start=now, period=period)
        trend.save()

        self.tags_dbo[tag] = trend

    def set_tags(self, tags, period):
        
        for tag in tags:

            self.set_tag(tag, period)
    
    def create_tables(self, tables):

        if not self._db:
            return
        self._db.create_tables(tables, safe=True)

    def drop_tables(self, tables, cascade=False):

        if not self._db:
            return

        self._db.drop_tables(tables, safe=True, cascade=True)

    def write_tag(self, tag, value):

        trend = self.tags_dbo[tag]

        tag_value = TagValue.create(tag=trend, value=value)
        tag_value.save()

    def read_tag(self, tag):
        
        query = TagTrend.select().order_by(TagTrend.start)
        trend = query.where(TagTrend.name == tag).get()
        
        period = trend.period
        values = trend.values.select()
        
        result = dict()

        t0 = values[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')
        values = [value.value for value in values]

        result["t0"] = t0
        result["dt"] = period
        result["values"] = values
        
        return result
