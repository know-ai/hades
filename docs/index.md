# PyHades
A python library to develop continuous tasks using sync or async concurrent threads

## Description
PyHades was born with the intention of solving synchronized or asynchronous concurrent tasks in an easy and declarative way.

Situations where the finite state machine design pattern is recommended, PyHades offers a declarative way to solve such a problem.

You can use PyHades for small, medium or even large projects, regardless of the type of application, that is, web, desktop, cloud, embedded development, among others.

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

    print('Hello wiht a 0.5 second period')

if __name__=='__main__':

    app.run()
```

## User Guide
You can define a PyHadesStateMachine to solve problem with this [Design Pattern](https://en.wikipedia.org/wiki/State_pattern#:~:text=The%20state%20pattern%20is%20a,concept%20of%20finite%2Dstate%20machines.)

- [State Machines]()