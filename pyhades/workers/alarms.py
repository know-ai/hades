# -*- coding: utf-8 -*-
"""rackio/workers/alarms.py

This module implements Alarm Worker.
"""
import logging
import time
from ..alarms import AlarmState
from datetime import datetime
from ..dbmodels import AlarmLogging as AlarmModel

from .worker import BaseWorker


class AlarmWorker(BaseWorker):

    def __init__(self, manager, period=1.0):

        super(AlarmWorker, self).__init__()
        
        self._manager = manager
        self._period = period

        self._manager.attach_all()

    def run(self):

        _queue = self._manager.get_queue()

        while True:

            time.sleep(self._period)

            for _, _alarm in self._manager._alarms.items():

                if _alarm.state == AlarmState.SHLVD:

                    _now = datetime.now()
                    if _alarm._shelved_until:
                        
                        if _now >= _alarm._shelved_until:
                            
                            AlarmModel.create(
                                name=_alarm.name,
                                state=_alarm.state.state,
                                priority=_alarm._priority,
                                value=_alarm._value
                            )
                            _alarm.unshelve()

            while not _queue.empty():

                item = _queue.get()
                
                _tag = item["tag"]
                self._manager.execute(_tag)

            if self.stop_event.is_set():
                break

        logging.info("Alarm worker shutdown successfully!")