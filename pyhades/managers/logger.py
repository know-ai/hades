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
    DataTypes,
    BaseModel)


class DBManager:
    r"""
    Database Manager class for database logging settings.
    """

    def __init__(self, period:float=1.0, delay:float=1.0, drop_tables:bool=False):

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
        r"""
        Initialize a new DB Object SQLite - Postgres - MySQL

        **Parameters**

        * **db** (db object): Sqlite - Postgres or MySql db object

        **Returns** `None`
        """
        self._logger.set_db(db)

    def get_db(self):
        r"""
        Returns a DB object
        """
        return self._logger.get_db()

    def set_dropped(self, drop_tables:bool):
        r"""
        Allows to you set a flag variable to drop database tables when run app.

        **Parameters**

        * **drop_tables** (bool) If True, drop all tables define in the app an initialized it in blank.

        **Returns**

        * **None**
        """
        self._drop_tables = drop_tables

    def get_dropped(self)->bool:
        r"""
        Gets flag variables to drop tables when initialize the app

        **Return**

        * **drop_tables** (bool) Flag variables to drop table
        """
        return self._drop_tables

    def register_table(self, cls:BaseModel):
        r"""
        Allows to you register a new database model

        **Parameters**

        * **cls* (BaseModel): A class that inherit from BaseModel

        """
        self._extra_tables.append(cls)

    def create_tables(self):
        r"""
        Creates default tables and tables registered with method *register_table*
        """
        self._tables.extend(self._extra_tables)

        self._logger.create_tables(self._tables)

    def drop_tables(self):
        r"""
        Drop all tables defined
        """
        tables = self._tables
        
        self._logger.drop_tables(tables)

    def clear_default_tables(self):
        r"""
        If you want initialize any PyHades app without default tables, you can use this method
        """
        self._tables = []

    def add_tag(
        self,
        tag:str, 
        unit:str, 
        data_type:str, 
        description:str, 
        min_value:float, 
        max_value:float, 
        tcp_source_address:str, 
        node_namespace:str, 
        period:float
    ):
        r"""
        Add tag to tag's repository
        """
        self._logging_tags.add_tag(
            tag, 
            unit, 
            data_type, 
            description, 
            min_value, 
            max_value, 
            tcp_source_address, 
            node_namespace, 
            period
        )

    def get_tags(self)->dict:
        r"""
        Gets all tag defined in tag's repository
        """
        return self.engine.get_tags()

    def set_tag(
        self, 
        tag:str, 
        unit:str, 
        data_type:str, 
        description:str, 
        min_value:float=None, 
        max_value:float=None, 
        tcp_source_address:str=None, 
        node_namespace:str=None):
        r"""
        Sets tag to Database

        **Parameters**

        * **tag** (str):
        * **unit** (str):
        * **data_type** (str):
        * **description** (str):
        * **min_value** (float)[Optional]:
        * **max_value** (float)[Optional]:
        * **tcp_source_address** (str)[Optional]:
        * **node_namespace** (str)[Optional]:
        """
        self._logger.set_tag(
            tag=tag,  
            unit=unit,
            data_type=data_type,
            description=description,
            min_value=min_value,
            max_value=max_value,
            tcp_source_address=tcp_source_address,
            node_namespace=node_namespace
        )

    def set_tags(self):
        r"""
        Allows to you define all tags added with *add_tag* method
        """
        for period in self._logging_tags.get_groups():
            
            tags = self._logging_tags.get_tags(period)
        
            for tag, unit, data_type, description, min_value, max_value, tcp_source_address, node_namespace in tags:

                self.set_tag(
                    tag=tag,
                    unit=unit, 
                    data_type=data_type, 
                    description=description, 
                    min_value=min_value, 
                    max_value=max_value, 
                    tcp_source_address=tcp_source_address, 
                    node_namespace=node_namespace)

    def get_table(self)->LogTable:
        r"""
        Gets a dictionary based Class to hold the tags to be logged.
        """
        return self._logging_tags
        
    def set_period(self, period:float):
        r"""
        Sets period to log into database

        **Parameters**

        * **period** (float): Time scan to log into database
        """
        self._period = period

    def get_period(self)->float:
        r"""
        Gets the period wich is scan into database

        **Returns**

        * **period** (float): Time scan to log into database
        """
        return self._period

    def set_delay(self, delay:float):
        r"""
        Sets an initial time to delay some time before start to logging database

        **Parameters**

        * **delay** (float): Time in seconds to delay before start to logging database
        """
        self._delay = delay

    def get_delay(self)->float:
        r"""
        Gets time to delay some time before start to logging database

        **Returns**

        * **delay** (float): Time in seconds to delay before start to logging database
        """
        return self._delay

    def init_database(self):
        r"""
        Initializes all databases.
        """
        if self.get_dropped():
            try:
                self.drop_tables()
            except Exception as e:
                error = str(e)
                logging.error("Database:{}".format(error))

        self.create_tables()

        self.set_tags()

    def summary(self)->dict:
        r"""
        Get database manager summary

        **Returns**

        * **summary** (dict): Database summary
        """
        result = dict()

        result["period"] = self.get_period()
        result["tags"] = self.get_tags()
        result["delay"] = self.get_delay()

        return result
    