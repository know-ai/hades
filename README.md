# PyHades
A python library to develop continuous tasks using sync or async concurrent threads, but not only that, the design intent for PyHades is create Automation Industrial Process Applications (AIPA); that's why, PyHades provides to you a Database model according to AIPA, currently, PyHades counts with Historian DataLogger and Alarm Management System (ISA 18.2).

## Description
PyHades was born with the intention of solving synchronized or asynchronous concurrent tasks in an easy and declarative way.

Situations where the finite state machine design pattern is recommended, PyHades offers a declarative way to solve such a problem.

You can use PyHades for small, medium or even large projects, regardless of the type of application, that is, web, desktop, cloud, embedded development, among others.

## Why you should use PyHades?

Imagine that you have 2 functions that you want to run like [daemons](https://en.wikipedia.org/wiki/Daemon_(computing))

```python
import time

def func1():
    
    while True:

        print("func1 running")
        time.sleep(1)

def func2():

    while True:

        print("func2 running")
        time.sleep(1)
```

You run these functions when run a main function.

```python
def main():
    
    func1()
    func2()

if __name__=='__main__':

    main()
```

Here you already have a problem, the *func2* is unreachable due to the blocking behavior of the *func1*.

PyHades solves to you this problem using multithreading in an easy and declarative way without blocking behavior.

```python
from pyhades import PyHades

app = PyHades()

@app.thread(period=1.0)
def func1():
    
    print("func1 running")

@app.thread(period=1.0)
def func2():

    print("func2 running")
    
if __name__=='__main__':

    app.run()
```

## Don't worry about the [GIL](https://realpython.com/python-gil/#:~:text=The%20Python%20Global%20Interpreter%20Lock%20or%20GIL%2C%20in%20simple%20words,at%20any%20point%20in%20time.)

The impact of the GIL isn’t visible to developers who execute single-threaded programs, but it can be a performance bottleneck in CPU-bound and multi-threaded code.

When it comes to multithreading, there are problems that need to be solved, that can be financially impactful, difficult to debug, and non-trivial for developers.

One of the most famous problem to be solved are [race conditions](https://stackoverflow.com/questions/34510/what-is-a-race-condition).

Let me cite an example from the literature *Learning concurrency in Python: Speed up your python code with clean, readable, and advanced concurrency techniques: Elliot Forbes.* That seems to me very important to understand how dangerous it could be
don't keep in mind race conditions.

*We imagine writing a banking application that updates your account balance whenever you deposit or withdraw any money from that account.*

*Imagine, we started with $2.000 in our bank account, and say we are about to receive a bonus of $5.000, because we managed to bug fix a concurrency issue in work was costing the business millions. Now also imagine that you are also to pay a rent of $1.000 on the same day.*

*If our banking application had two processes, one of which dealt with the witdrawing, Process A, and the other wich dealt with the depositing, Process B. Say Process B, which deals with deposits into your account, reads your bank balance as $2.000. If Process A was to start its withdrawal for the rent just after Process B starts its transaction, it would see the starting balance as $2.000. Process B would then complete its transaction, and correctly add $5.000 to our starting $2.000, and we'd be left with the grand sum of $7.000.*

*However, since Process A started its transaction thinking that the satrting balance was $2.000, it would unwittingly leave us bonus-less when it updates our final bank balance to $1.000. This is a prime example of a race condition within our software, and it's a very real danger always waiting to strike us in the most unfortunate ways.*

So, **this problem is solved with PyHades with its read/write methods in a safe-thread mechanism.** 

Let's take a look at what happened in closer detail. If we look at the following table, we'll see the ideal flow of execution for both Process A and Process B:

![safe-thread mechanism](img/safe-thread-mechanism.png)

However, due to the fact we haven't implemented proper synchronization mechanisms to protect our account balance, Process A and Process B actually followed the following execution path and gave us an erroneous result:

![unsafe-thread mechanism](img/unsafe-thread-mechanism.png)

## Installation
You can install PyHades from PyPi
```python
pip install PyHades
```

## Quick Start
PyHades is based on Singleton Pattern, so you can instantiate it anywhere in your app and it will keep its reference and be the same object throughout your app.

```python
from pyhades import PyHades

app = PyHades()

@app.thread(period=0.5)
def say_hello():

    print('Hello with a 0.5 second period')

if __name__=='__main__':

    app.run()
```

## User Guide
You can define a PyHadesStateMachine to solve problem with this [Design Pattern](https://en.wikipedia.org/wiki/State_pattern#:~:text=The%20state%20pattern%20is%20a,concept%20of%20finite%2Dstate%20machines.)

- [State Machines](https://hades.readthedocs.io/en/latest/user_guide_state_machines)
- [Current Value Table](https://hades.readthedocs.io/en/latest/user_guide_cvt)