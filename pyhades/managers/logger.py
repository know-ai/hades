# -*- coding: utf-8 -*-
"""pyhades/managers/logger.py

This module implements Logger Manager.
"""
import logging
from ..logger import DataLoggerEngine, LogTable
from ..tags import CVTEngine
from ..dbmodels import (
    Tags, 
    TagValue, 
    AlarmTypes, 
    AlarmPriorities, 
    AlarmStates, 
    AlarmsDB, 
    AlarmLogging, 
    AlarmSummary, 
    Variables, 
    Units, 
    DataTypes)


class DBManager:
    """Database Manager class for database logging settings.
    """

    def __init__(self, period=1.0, delay=1.0, drop_tables=False):

        self._period = period
        self._delay = delay
        self._drop_tables = drop_tables
        self.engine = CVTEngine()

        self._logging_tags = LogTable()
        self._logger = DataLoggerEngine()
        self._tables = [
            Variables, 
            Units, 
            DataTypes, 
            Tags, 
            TagValue, 
            AlarmTypes,
            AlarmStates,
            AlarmPriorities,
            AlarmsDB,
            AlarmLogging, 
            AlarmSummary
        ]

        self._extra_tables = []

    def set_db(self, db):

        self._logger.set_db(db)

    def get_db(self):

        return self._logger.get_db()

    def set_dropped(self, drop_tables):

        self._drop_tables = drop_tables

    def get_dropped(self):

        return self._drop_tables

    def register_table(self, cls):

        self._extra_tables.append(cls)

    def create_tables(self):

        self._tables.extend(self._extra_tables)

        self._logger.create_tables(self._tables)

    def drop_tables(self):

        tables = self._tables
        
        self._logger.drop_tables(tables)

    def clear_default_tables(self):

        self._tables = []

    def add_tag(
        self,
        tag, 
        unit, 
        data_type, 
        desc, 
        min_value, 
        max_value, 
        tcp_source_address, 
        node_namespace, 
        period
    ):
        
        self._logging_tags.add_tag(
            tag, 
            unit, 
            data_type, 
            desc, 
            min_value, 
            max_value, 
            tcp_source_address, 
            node_namespace, 
            period
        )

    def get_tags(self):

        return self.engine.get_tags()

    def set_tag(
        self, 
        tag, 
        unit:str, 
        data_type:str, 
        desc:str, 
        min_value:float=None, 
        max_value:float=None, 
        tcp_source_address:str=None, 
        node_namespace:str=None):

        self._logger.set_tag(
            tag=tag,  
            unit=unit,
            data_type=data_type,
            desc=desc,
            min_value=min_value,
            max_value=max_value,
            tcp_source_address=tcp_source_address,
            node_namespace=node_namespace
        )

    def set_tags(self):

        for period in self._logging_tags.get_groups():
            
            tags = self._logging_tags.get_tags(period)
        
            for tag, unit, data_type, desc, min_value, max_value, tcp_source_address, node_namespace in tags:

                self.set_tag(
                    tag=tag,
                    # period=period, 
                    unit=unit, 
                    data_type=data_type, 
                    desc=desc, 
                    min_value=min_value, 
                    max_value=max_value, 
                    tcp_source_address=tcp_source_address, 
                    node_namespace=node_namespace)

    def get_table(self):

        return self._logging_tags
        
    def set_period(self, period):

        self._period = period

    def get_period(self):

        return self._period

    def set_delay(self, delay):

        self._delay = delay

    def get_delay(self):

        return self._delay

    def init_database(self):
    
        if self.get_dropped():
            try:
                self.drop_tables()
            except Exception as e:
                error = str(e)
                logging.error("Database:{}".format(error))

        self.create_tables()

        self.set_tags()

    def summary(self):

        result = dict()

        result["period"] = self.get_period()
        result["tags"] = self.get_tags()
        result["delay"] = self.get_delay()

        return result
    