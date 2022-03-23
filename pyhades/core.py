r"""
pyhades/core.py

This module implements the core app class and methods for PyHades
"""
import time
import sys
import logging
import concurrent.futures
from datetime import datetime

from ._singleton import Singleton

from .workers import _ContinuosWorker, StateMachineWorker

from .managers import StateMachineManager

class PyHades(Singleton):
    r"""
    
    Usage:
    
    ```python
    >>> from pyhades import PyHades
    >>> app = PyHades()
    ```

    """

    def __init__(self):
        r"""
        Documentation here
        """
        self._start_up_datetime = ""
        self._mode = 'development'
        self._logging_level = logging.INFO
        self._log_file = ""
        self._thread_functions = list()
        self._max_threads = 20
        self._threads = None
        self.workers = list()

        self._machine_manager = StateMachineManager()

    def set_start_up_datetime(self, value):
        r"""
        Documentation here
        """
        self._start_up_datetime = value

    def get_start_up_datetime(self):
        r"""
        Documentation here
        """

        return self._start_up_datetime

    def set_mode(self, mode):
        r"""
        Documentation here
        """

        self._mode = mode
    
    def get_mode(self):
        r"""
        Documentation here
        """

        return self._mode

    def set_log(self, level=logging.INFO, file=""):
        r"""
        Sets the log file and level.
        
        **Parameters:**
        
        * **level** (str): `logging.LEVEL`.
        * **file** (str): log filename.

        **Returns:** `None`

        Usage:

        ```python
        >>> app.set_log(file="app.log")
        ```
        """

        self._logging_level = level
        
        if file:

            self._log_file = file

    def set_threads(self, nthreads):
        r"""
        Documentation here
        """
        self._max_threads = nthreads

    def append_machine(self, machine, interval=1, mode="sync"):
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
        """

        return self._machine_manager.get_machine(name)

    def get_machines(self):
        """
        Returns All PyHades State Machine defined.
        """

        return self._machine_manager.get_machines()

    def define_machine(self, name="", interval=1, mode="sync", **kwargs):
        """
        Append a state machine to the state machine manager
        by a class decoration.
        
        **Parameters:**
        
        * **interval** (int): Interval execution time in seconds.
        """

        def decorator(cls):

            machine = cls(name, **kwargs)
            
            self.append_machine(machine, interval=interval, mode=mode)

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

    def _start_threads(self):
        r"""
        Documentation here
        """

        _max = self._max_threads
        self._scheduler = concurrent.futures.ThreadPoolExecutor(max_workers=_max)

        for _f in self._thread_functions:

            try:
                self.workers.append(self._scheduler.submit(_f))
            except Exception as e:
                message = "Error on continous functions worker start-up"

    def _stop_threads(self):

        for worker in self._thread_functions:
            try:
                worker.stop()
            except Exception as e:
                message = "Error on wokers stop"
                print(e, message)

    def _start_workers(self):

        _machine_worker = StateMachineWorker(self._machine_manager)

        try:

            workers = [
                _machine_worker, 
            ]

            for worker in workers:

                worker.daemon = True
                worker.start()

        except Exception as e:
            message = "Error on wokers start-up"
            print(e, message)

        self.workers = workers

    def stop_workers(self):

        for worker in self.workers:
            try:
                worker.stop()
            except Exception as e:
                message = "Error on wokers stop"
                print(e, message)

    def run(self):
        r"""
        Documentation here
        """
        _start_up_datetime = datetime.now()
        self.set_start_up_datetime(_start_up_datetime)

        self._start_workers()
        self._start_threads()

        try:         
            while True:

                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            print("Manual Shutting down!!!")
            self._stop_threads()
            self.stop_workers()
            time.sleep(1)
            sys.exit()
            
            