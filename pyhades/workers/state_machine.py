# -*- coding: utf-8 -*-
"""pyhades/workers/state.py

This module implements State Machine Worker.
"""
import heapq
import logging
from statistics import mode
import time

from ..utils import log_detailed

from collections import deque
from threading import Thread

from .worker import BaseWorker


class MachineScheduler():

    def __init__(self):

        self._ready = deque()
        self._sleeping = list()
        self._sequence = 0
        self._stop = False

    def call_soon(self, func):
        
        self._ready.append(func)

    def call_later(self, delay, func, machine):
        
        self._sequence += 1
        deadline = time.time() + delay
        heapq.heappush(self._sleeping, (deadline, self._sequence, func, machine))

    def stop(self):

        self._stop = True
    
    def run(self):
        while self._ready or self._sleeping:

            if self._stop:
                break

            if not self._ready:
                deadline, _, func, machine = heapq.heappop(self._sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                else:
                    logging.warning(f"State Machine: {machine.name} not executed on time...")  
                self._ready.append(func)

            while self._ready:
                func = self._ready.popleft()
                func()


class SchedThread(Thread):

    def __init__(self, machine, interval):

        super(SchedThread, self).__init__()

        self.machine = machine
        self.interval = interval

    def stop(self):

        self.scheduler.stop()

    def loop_closure(self, machine, interval, scheduler):

        def loop():
            machine.loop()
            local_interval = machine.get_state_interval()
            interval = machine.get_interval()
            interval = min(interval, local_interval)
            scheduler.call_later(interval, loop, machine)

        return loop
    
    def target(self, machine, interval):

        scheduler = MachineScheduler()
        self.scheduler = scheduler

        func = self.loop_closure(machine, interval, scheduler)
        scheduler.call_soon(func)
        
        scheduler.run()        

    def run(self):

        self.target(self.machine, self.interval)


class AsyncStateMachineWorker(BaseWorker):

    def __init__(self):

        super(AsyncStateMachineWorker, self).__init__()

        self._machines = list()
        self._schedulers = list()

        self.jobs = list()

    def add_machine(self, machine, interval):

        self._machines.append((machine, interval,))

    def run(self):

        for machine, interval in self._machines:

            sched = SchedThread(machine, interval,)

            self._schedulers.append(sched)

        for sched in self._schedulers:

            sched.daemon = True
            sched.start()

    def stop(self):

        for sched in self._schedulers:
            try:
                sched.stop()
            except Exception as e:
                message = "Error on async scheduler stop"
                log_detailed(e, message)
    

class StateMachineWorker(BaseWorker):

    def __init__(self, manager):

        super(StateMachineWorker, self).__init__()
        
        self._manager = manager
        self._sync_scheduler = MachineScheduler()
        self._async_scheduler = AsyncStateMachineWorker()

        self.jobs = list()

    def __str__(self):
        state_machines = self._manager.get_machines()
        result = ''

        for state_machine, interval, mode in state_machines:

            result += state_machine.info() + '\n'
        
        return result

    def loop_closure(self, machine, interval):

        self._machine = machine
        
        def loop():
            machine.loop()
            local_interval = machine.get_state_interval()
            interval = machine.get_interval()
            interval = min(interval, local_interval)
            self._sync_scheduler.call_later(interval, loop)

        return loop

    def run(self):

        for machine, interval, mode in self._manager.get_machines():
            logging.info(f"State Machine: {machine.name} started")
            if mode == "async":
                self._async_scheduler.add_machine(machine, interval)
            else:
                func = self.loop_closure(machine, interval)
                self._sync_scheduler.call_soon(func)
        
        self._async_scheduler.run()
        self._sync_scheduler.run()

    def stop(self):

        self._async_scheduler.stop()
        self._sync_scheduler.stop()
    