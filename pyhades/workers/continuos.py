# -*- coding: utf-8 -*-
"""pyhades/workers/continuos.py

This module implements Continuos Worker.
"""
import time
import logging

STOP = "Stop"
PAUSE = "Pause"
RUNNING = "Running"
ERROR = "Error"


class _ContinuosWorker:

    def __init__(self, f, worker_name=None, period=1.0, error_message=None):

        self._f = f

        if not worker_name:
            worker_name = f.__name__

        self._name = worker_name
        self._period = period

        self._error_message = error_message
        self._status = STOP       # [STOP, PAUSE, RUNNING, ERROR]

        self.last = None

        from ..core import PyHades

        hades = PyHades()
        hades._thread_functions.append(self)

    def __str__(self):
        return f'''\nThread Name: {self._name} - Period: {self._period} seconds - Status: {self._status}'''

    def serialize(self):

        result = dict()
        result["name"] = self._name
        result["period"] = self._period
        result["status"] = self._status

        return result
    
    def set_last(self):

        self.last = time.time()

    def sleep_elapsed(self):

        elapsed = time.time() - self.last

        if elapsed < self._period:
            time.sleep(self._period - elapsed)
        else:
            logging.warning(f"Worker {self._name}: Failed to execute task on time...")

        self.set_last()

    def get_name(self):

        return self._name

    def get_status(self):

        return self._status

    def log_error(self, e):
        
        error = str(e)

        if self._error_message:
            logging.error("Worker - {}:{}:{}".format(self._name, self._error_message, error))
        else:
            logging.error("Worker - {}:{}".format(self._name, error))
    
    def stop(self):

        self._status = STOP

    def __call__(self, *args):

        self.set_last()

        self._status = RUNNING

        try:

            while True:

                if self._status == STOP:

                    return
                
                else:

                    self._status = RUNNING
                    try:
                        self._f()
                    except Exception as e:
                        
                        self.log_error(e)
                        self._status = ERROR

                self.sleep_elapsed()
        
        except (KeyboardInterrupt, SystemExit):
            
            self._status = STOP