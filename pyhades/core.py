r"""
pyhades/core.py

This module implements the core app class and methods for PyHades
"""
import time
import sys
import logging
import concurrent.futures
from datetime import datetime
import os

from .alarms import Alarm, TriggerType

from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase

from .utils import log_detailed, parse_config

from ._singleton import Singleton

from .workers import _ContinuosWorker, StateMachineWorker, LoggerWorker, AlarmWorker

from .managers import StateMachineManager, DBManager, AlarmManager

from .tags import CVTEngine

from .dbmodels import SQLITE, POSTGRESQL, MYSQL
# PyHades Status

STARTED = 'Started'
RUNNING = 'Running'
STOPPED = 'Stopped'

DEVELOPMENT_MODE = 'Development'
PRODUCTION_MODE = 'Production'

APP_MODES = [DEVELOPMENT_MODE, PRODUCTION_MODE]


class PyHades(Singleton):
    r"""
    PyHades is a [singleton](https://en.wikipedia.org/wiki/Singleton_pattern) class to develop multi threads web application 
    for general purposes .

    Usage:
    
    ```python
    >>> from pyhades import PyHades
    >>> app = PyHades()
    ```
    """

    def __init__(self):

        self._start_up_datetime = None
        self._status = STARTED
        self._logging_level = logging.INFO
        self._max_threads = 10
        self._log_file = "app.log"
        self._thread_functions = list()
        self._threads = list()
        self.workers = list()
        self._mode = DEVELOPMENT_MODE
        self._sio = None

        self._machine_manager = StateMachineManager()
        self._db_manager = DBManager()
        self._engine = CVTEngine()
        self._alarm_manager = AlarmManager()

        self.db = None

    def info(self):
        r"""
        Shows a summary threads on execution
        """
        return f'''
        \nPyHades {self._status}\n
        \n* Threads Running: {self.threads_running()}
        {self.threads_info()}
        \n* State Machines Running: {self.state_machines_running()}
        {self.state_machines_info()}
        '''

    def set_mode(self, mode:str):
        r"""
        Allows to you define "Development" or "Production" mode.

        For Development mode you use Sqlitedatabase by default when you define it.

        For Production mode you can use Sqlite - Postgres - MySQL

        **Parameters**

        * **mode** (str): App mode ('Development' or 'Production')

        **Return** `None`

        ```python
        >>> app = PyHades()
        >>> app.set_mode('Development')
        ```
        """
        if mode.capitalize() in APP_MODES:
            self._mode = mode

    def get_mode(self):
        r"""
        Gets app mode

        **Returns**
        
        * **mode** (str)

        ```python
        >>> app.get_mode()
        'Development'
        ```
        """
        return self._mode

    def set_socketio(self, sio):

        self._sio = sio

    def get_socketio(self):

        return self._sio

    def threads_running(self):
        r"""
        Gets thread numbers defined in the app

        **Returns:** (int)

        Usage

        ```python
        >>> threads_running = app.threads_running()
        ```
        """
        return len(self._thread_functions)

    def state_machines_running(self):
        r"""
        Gets state machines numbers defined in the app

        **Returns:** (int)

        Usage

        ```python
        >>> state_machines_running = app.state_machines_running()
        ```
        """
        return len(self.workers)

    def threads_info(self):
        r"""
        Gets information of all defined threads

        **Returns:** (str)

        Usage

        ```python
        >>> app.threads_info()
        ```
        """
        result = ''

        for _thread in self._thread_functions:

            result += _thread.__str__()

        return result

    def state_machines_info(self):
        r"""
        Gets information of all defined state machines

        **Returns:** (str)

        Usage

        ```python
        >>> app.state_machines_info()
        ```
        """
        result = ''

        for _state_machine_worker in self.workers:

            result = _state_machine_worker.__str__()
            break

        return result

    def _set_start_up_datetime(self, date_time:datetime=datetime.now()):
        r"""
        Sets start up datetime of the application

        **Parameters**

        * **date_time** (datetime): date_time when the application is start up (default value is datetime.now())

        **Returns:** `None`

        Usage
        ```python
        >>> app._set_start_up_datetime()
        ```
        """
        self._start_up_datetime = date_time

    def get_start_up_datetime(self):
        r"""
        Gets the start up datetime of the application

        **Returns**

        * **date_time** (datetime): Start up datetime of the app

        Usage

        ```python
        >>> start_up = app.get_start_up_datetime()
        ```
        """

        return self._start_up_datetime

    def append_table(self, table):
        """
        Append a database model class definition.
        
        **Parameters:**

        * **table** (BaseModel): A Base Model Inheritance.
        """

        self._db_manager.register_table(table)

    def define_table(self, cls):
        """
        Append a database model class definition
        by a class decoration.
        """

        self.append_table(cls)

        return cls

    def set_log(self, level=logging.INFO, file:str="app.log"):
        r"""
        Sets the log file and level.
        
        **Parameters:**
        
        * **level** (str): `logging.LEVEL` (default: logging.INFO).
        * **file** (str): log filename (default: 'app.log').

        **Returns:** `None`

        Usage:

        ```python
        >>> app.set_log(file="app.log")
        ```
        """

        self._logging_level = level
        
        if file:

            self._log_file = file

    def drop_db(self, dbfile):

        files = [dbfile]
        files.append(f"{dbfile}-shm")
        files.append(f"{dbfile}-wal")

        for file in files:

            if os.path.exists(file):
                
                os.remove(file)

    def set_db_from_config_file(self, config_file):
        r"""
        Documention here
        """
        config = parse_config(config_file)

        if 'db' in config:

            app_mode = self.get_mode()
            db_config = config['db']

            if app_mode == DEVELOPMENT_MODE:

                if 'dev_mode' in db_config:
                    dev_db_config = db_config['dev_mode']
                    self.set_db(dbtype=SQLITE, dbfile=dev_db_config['db_file'])

                else:

                    logging.error(f"You must define dev_mode key in db configuration in your config file")

            else:
                if 'prod_mode' in db_config:
                    prod_db_config = db_config['prod_mode']
                    DATABASE = {
                        'user': prod_db_config['db_user'],
                        'password': prod_db_config['db_password'],
                        'host': prod_db_config['db_host'],
                        'port': prod_db_config['db_port'],
                        'name': prod_db_config['db_name']
                        }
                    self.set_db(dbtype=prod_db_config['db_type'], **DATABASE)

                else:

                    logging.error(f"You must define prod_mode key in db configuration in your config file")
            
            self.set_dbtags(self._engine._cvt._tags, db_config['sample_time'], delay=db_config['delay'])
            self._db_manager.create_tables()
            self.init_db()

    def set_db(self, dbtype:str=SQLITE, drop_table=False, clear_default_tables=False, **kwargs):
        """
        Sets the database, it supports SQLite and Postgres,
        in case of SQLite, the filename must be provided.

        if app mode is "Development" you must use SQLite Databse
        
        **Parameters:**

        * **dbfile** (str): a path to database file.
        * *drop_table** (bool): If you want to drop table.
        * **cascade** (bool): if there are some table dependency, drop it as well
        * **kwargs**: Same attributes to a postgres connection.

        **Returns:** `None`

        Usage:

        ```python
        >>> app.set_db(dbfile="app.db")
        ```
        """

        from .dbmodels import proxy

        if clear_default_tables:

            self._db_manager.clear_default_tables()

        if self.get_mode() == DEVELOPMENT_MODE:

            dbfile = kwargs.get("dbfile", ":memory:")

            self._db = SqliteDatabase(dbfile, pragmas={
                'journal_mode': 'wal',
                'journal_size_limit': 1024,
                'cache_size': -1024 * 64,  # 64MB
                'foreign_keys': 1,
                'ignore_check_constraints': 0,
                'synchronous': 0}
            )

        elif dbtype.lower() == SQLITE:

            dbfile = kwargs.get("dbfile", ":memory:")
            
            self._db = SqliteDatabase(dbfile, pragmas={
                'journal_mode': 'wal',
                'journal_size_limit': 1024,
                'cache_size': -1024 * 64,  # 64MB
                'foreign_keys': 1,
                'ignore_check_constraints': 0,
                'synchronous': 0}
            )

        elif dbtype.lower() == MYSQL:
            
            db_name = kwargs['name']
            del kwargs['name']
            self._db = MySQLDatabase(db_name, **kwargs)

        elif dbtype.lower() == POSTGRESQL:
            
            db_name = kwargs['name']
            del kwargs['name']
            self._db = PostgresqlDatabase(db_name, **kwargs)
        
        proxy.initialize(self._db)
        self._db_manager.set_db(self._db)
        self._db_manager.set_dropped(drop_table)

    def set_dbtags(self, tags, period=0.5, delay=1.0):
        """
        Sets the database tags for logging.

        If you want to log any tag defined in CVTengine, you must define it here
        
        **Parameters:**

        * **tags** (list): A list of the tags.

        **Returns:** `None`

        Usage:

        ```python
        >>> tags = ["P1", "P2", "T1"]
        >>> app.set_dbtags(tags, period=1.0)
        ```
        """

        self._db_manager.set_period(period)
        self._db_manager.set_delay(delay)

        for tag_name, tag_object in tags.items():
            unit = tag_object.get_unit()
            data_type = tag_object.get_data_type()
            desc = tag_object.get_description()
            min_value = tag_object.get_min_value()
            max_value = tag_object.get_max_value()
            tcp_source_address = tag_object.get_tcp_source_address()
            node_namespace = tag_object.get_node_namespace()

            self._db_manager.add_tag(
                tag_name, 
                unit, 
                data_type, 
                desc, 
                min_value, 
                max_value, 
                tcp_source_address, 
                node_namespace, 
                period
            )

    def get_dbtags(self):
        """
        Returns the database tags for logging.
        """

        return self._db_manager.get_tags()

    def set_max_threads(self, max_threads:int):
        r"""
        Sets maximum numbers of threads

        **Parameters**

        * **max_threads** (int): Max numbers of threads

        **Returns** `None`

        Usage

        ```python
        >>> app.set_max_threads(20)
        ```
        """
        self._max_threads = max_threads

    def _append_machine(self, machine, interval=1, mode="sync"):
        """
        Append a state machine to the state machine manager.
        
        **Parameters:**

        * **machine** (`PyHadesStateMachine`): a state machine object.
        * **interval** (int): Interval execution time in seconds.
        """
        machine.set_interval(interval)
        self._machine_manager.append_machine(machine, interval=interval, mode=mode)

    def get_machine(self, name):
        """
        Returns a PyHades State Machine defined by its name.
        
        **Parameters:**
        
        * **name** (str): a pyhades state machine name.

        Usage

        ```python
        >>> state_machine = app.get_machine('state_machine_name')
        ```
        """

        return self._machine_manager.get_machine(name)

    def get_machines(self):
        """
        Returns all defined PyHades state machines.

        **Returns** (list)

        Usage

        ```python
        >>> state_machines = app.get_machines()
        ```
        """

        return self._machine_manager.get_machines()

    def get_state_machine_manager(self):
        r"""
        Gets state machine Manager

        **Returns:** StateMachineManager instance

        ```python
        >>> app.get_state_machine_manager()
        ```
        """
        return self._machine_manager

    def get_db_manager(self):
        r"""
        Gets DB Manager

        **Returns:** DBManager instance

        ```python
        >>> app.db_manager()
        ```
        """
        return self._db_manager

    def define_alarm_from_config_file(self, config_file):
        r"""
        Documentation here
        """
        config = parse_config(config_file)

        if 'alarms' in config['modules']:

            alarms = config['modules']['alarms']
            self._alarm_manager.load_alarms_from_db()
            self.__set_config_alarms(alarms)

        else:

            logging.warning(f"You must define alarms key in your config file")

    def __set_config_alarms(self, alarms):
        r"""
        Documentaion here
        """
        _alarms = self._alarm_manager.get_alarms()
        manager_alarms = [alarm.name for id, alarm in _alarms.items()]
        for _, attrs in alarms.items():

            name = attrs['name']
            tag = attrs['tag']
            desc = attrs['desc']
            _type = attrs['type']
            trigger = attrs['trigger']

            if name not in manager_alarms:

                alarm = Alarm(name, tag, desc)
                _trigger = TriggerType(_type.upper())
                alarm.set_trigger(value=trigger, _type=_trigger.value)
                self.append_alarm(alarm)

    def get_alarm_manager(self):
        r"""
        Gets DB Manager

        **Returns:** AlarmManager instance

        ```python
        >>> app.alarm_manager()
        ```
        """
        return self._alarm_manager

    def append_alarm(self, alarm):
        """
        Append an alarm to the alarm manager.
        
        **Parameters:**

        * **alarm** (`Alarm`): an alarm object.
        """

        self._alarm_manager.append_alarm(alarm)

    def get_alarm(self, name):
        """
        Returns a Alarm defined by its name.
        
        **Parameters:**

        * **name** (str): an alarm name.
        """

        alarm = self._alarm_manager.get_alarm(name)

        return alarm

    def get_alarm_by_tag(self, tag):
        """
        Returns a Alarm defined by its tag.

        **Parameters:**

        * **tag** (str): an alarm tag.
        """

        alarm = self._alarm_manager.get_alarm_by_tag(tag)

        return alarm

    def get_manager(self, name:str='state'):
        """
        Returns a specified application manager.
        
        **Parameters:**
        
        * **name** (str): a manager name.
        """
        if name == "alarm":
            manager = self.get_alarm_manager()
        elif name == "state":
            manager = self.get_state_machine_manager()
        elif name == 'db':
            manager = self.get_db_manager()

        return manager

    def define_machine(self, name="", interval=1, mode="sync", **kwargs):
        """
        Append a state machine to the state machine manager
        by decoration.
        
        **Parameters:**
        
        * **name** (str): State machine name
        * **interval** (int): Interval execution time in seconds.
        * **mode** (str): Syncronic or Asyncronic thread mode - allowed values ['sync', 'async'] 

        **Returns** Class (cls)

        Usage

        ```python
        >>> from pyhades import PyHades, PyHadesStateMachine
        >>> app = PyHades()
        >>> @app.define_machine(name='state_machine_name', interval=1, mode='async')
            class StateMachine(PyHadesStateMachine):
                ...
        ```
        """
        def decorator(cls):

            machine = cls(name, **kwargs)
            
            self._append_machine(machine, interval=interval, mode=mode)

            return cls

        return decorator

    def thread(self, function=None, **kwargs):
        r"""
        Decorator method to register functions plugins.
        
        This method will register into the PyHades application
        a new function to be executed by the Thread Pool Executor

        **Parameters:**

        * **period** (float): Value of the default loop execution time.
        
        **Returns:** `None`

        Usage:
    
        ```python
        @app.thread(period=0.5)
        def hello():
            print("Hello!!!")

        @app.thread
        def hello_world():
            print("Hello World!!!")
        ```
        """
        if function:
            return _ContinuosWorker(function)
        else:

            def wrapper(function):
                return _ContinuosWorker(function, **kwargs)

            return wrapper

    def _start_logger(self):
        r"""
        Starts logger in log file
        """
        log_format = "%(asctime)s:%(levelname)s:%(message)s"

        level = self._logging_level
        log_file = self._log_file

        if not log_file:
            logging.basicConfig(level=level, format=log_format)
            return
        
        logging.basicConfig(filename=log_file, level=level, format=log_format)

    def _start_threads(self):
        r"""
        Starts execution of the threads define by the decorator @app.thread
        """

        _max = self._max_threads
        self._scheduler = concurrent.futures.ThreadPoolExecutor(max_workers=_max)

        for _f in self._thread_functions:

            try:
                logging.info(f"Thread {_f._name} started")
                self._threads.append(self._scheduler.submit(_f))
            except Exception as e:
                message = "Error on continous functions worker start-up"
                log_detailed(e, message)

    def _stop_threads(self):
        r"""
        Safe stop execution of the defined threads
        """

        for worker in self._thread_functions:
            try:
                worker.stop()
            except Exception as e:
                message = "Error on wokers stop"
                log_detailed(e, message)
    
    def init_db(self):

        db_worker = LoggerWorker(self._db_manager)
        db_worker.init_database()

        try:

            db_worker.daemon = True
            db_worker.start()

        except Exception as e:
            message = "Error on db worker start-up"
            log_detailed(e, message)

        return db_worker

    def stop_db(self, db_worker):
        try:
            db_worker.stop()
        except Exception as e:
            message = "Error on db worker stop"
            log_detailed(e, message)

    def _start_workers(self):
        r"""
        Starts defined workers like State Machines.
        """
        db_worker = LoggerWorker(self._db_manager)
        db_worker.init_database()
        self.workers.append(db_worker)

        # AlarmWorker
        alarm_manager = self.get_alarm_manager()
        if len(alarm_manager.get_alarms())>0:

            alarm_worker = AlarmWorker(alarm_manager)
            self.workers.append(alarm_worker)

        # StateMachine Worker
        state_manager = self.get_state_machine_manager()
        if state_manager.exist_machines():

            state_worker = StateMachineWorker(state_manager)
            self.workers.append(state_worker)

        try:
            
            for worker in self.workers:
                worker.daemon = True
                worker.start()

        except Exception as e:
            message = "Error on workers start-up"
            log_detailed(e, message)

    def _stop_workers(self):
        r"""
        Safe stop workers execution like State Machines
        """
        for worker in self.workers:
            try:
                worker.stop()
            except Exception as e:
                message = "Error on wokers stop"
                log_detailed(e, message)

    def safe_start(self):
        r"""
        Run the app without a main thread, only run the app with the threads and state machines define
        """
        _start_up_datetime = datetime.now()
        self._set_start_up_datetime(_start_up_datetime)
        self._start_logger()
        self._start_workers()
        self._start_threads()

        logging.info("Hades started")  
        self._status = RUNNING
        logging.info(self.info()) 

    def safe_stop(self):
        r"""
        Stops the app in safe way with the threads
        """
        self._stop_threads()
        self._stop_workers()
        logging.info("Manual Shutting down")
        self._status = STOPPED
        sys.exit()

    def run(self):
        r"""
        Runs main app thread and all defined threads by decorators and State Machines besides this method starts app logger

        **Returns:** `None`

        Usage

        ```python
        >>> app.run()
        ```
        """
        self.safe_start()
        
        try: 
            
            while True:

                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            
            self.safe_stop()
            