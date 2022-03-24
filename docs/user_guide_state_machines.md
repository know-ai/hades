# PyHadesStateMachine

You can create your own State Machine Classes by inherit from PyHadesStateMachine.

In addition, you must decorate your class with the *define_machine* decorator in your PyHades app. This decorator need the following
parameters:

- name (str): State Machine name.
- interval (float or int): State machine interval for the thread loop.
- mode (str): Concurrent mode (sync or async)

```python
from pyhades import PyHades, PyHadesStateMachine, State

app = PyHades()

@app.define_machine(name='State Machine Name', interval=1.0, mode="async")
class StateMachineClass(PyHadesStateMachine):
    ...
```

Then, you must define the states of your state machine in the class context using the State class from pyhades.

```python
@app.define_machine(name='State Machine Name', interval=1.0, mode="async")
class StateMachineClass(PyHadesStateMachine):
    # states
    state_1 = State('State1', initial=True)
    state_2 = State('State2')
    ...
```

The *State* class need the state name as a string as a first argument, and the initial argument as optional if the state is the initial state.

Another topic that you make sure is to define the transitions.

For that, you use the *.to* method that has the state object

```python
@app.define_machine(name='State Machine Name', interval=1.0, mode="async")
class StateMachineClass(PyHadesStateMachine):
    ...
    # transition
    transition_1 = state_1.to(state_2)
    transition_2 = state_2.to(state_1)
    ...
```

You must define your class __init__ method with the following minimum content:

```python
@app.define_machine(name='State Machine Name', interval=1.0, mode="async")
class StateMachineClass(PyHadesStateMachine):
    ...
    def __init__(self, name):

        super().__init__(name)

    ...
```

The next step is to define the methods for states and transitions. 

The action that you want to be executed when the state machine is in some specific state must be defined in a method that begins with the word *while_* followed by the previously defined state object.

```python
@app.define_machine(name='State Machine Name', interval=1.0, mode="async")
class StateMachineClass(PyHadesStateMachine):
    ...
    def while_state_1(self):

        ...

    ...
```

Whereas whatever you want to be executed when the state machine is at the time of the transition, you must define the method by prepending the word *on_* followed by the previously defined transition object.

```python
@app.define_machine(name='State Machine Name', interval=1.0, mode="async")
class StateMachineClass(PyHadesStateMachine):
    ...
    def on_transition_1(self):

        ...

    ...
```

Below is a more concrete example applied to the scenario of a traffic light.

## Traffic Lights

```python
from pyhades import PyHades, PyHadesStateMachine, State

app = PyHades()

@app.define_machine(name='TrafficLight', interval=1.0, mode="async")
class TrafficLightMachine(PyHadesStateMachine):

    # states
    green  = State('Green', initial=True)
    yellow  = State('Yellow')
    red  = State('Red')

    # transitions
    slowdown = green.to(yellow)
    stop = yellow.to(red)
    go = red.to(green)

    # parameters
    time_left = 30

    def __init__(self, name):

        super().__init__(name)

    def on_slowdown(self):

        self.time_left = 3

    def on_stop(self):

        self.time_left = 20

    def on_go(self):

        self.time_left = 30

    def while_green(self):

        print(self)
        if self.time_left == 0:

            self.slowdown()

        self.time_left -= 1

    def while_yellow(self):

        print(self)
        if self.time_left == 0:

            self.stop()

        self.time_left -= 1

    def while_red(self):

        print(self)
        if self.time_left == 0:

            self.go()
        
        self.time_left -= 1

    def __str__(self):

        return f"{self.name}: {self.get_state()} - {self.time_left} second left."

if __name__=='__main__':

    app.run()
```

# State Machine with Flask

Many times, you have to execute this design pattern embedded in a web application.

In this section I show you how to integrate a state machine in an application with Flask

```python
from flask import Flask
from pyhades import PyHades, PyHadesContext, State, PyHadesStateMachine


flask_app = Flask(__name__)
hades_app = PyHades()

@hades_app.define_machine(name='TrafficLight', interval=1.0, mode="async")
class TrafficLightMachine(PyHadesStateMachine):

    # states
    green  = State('Green', initial=True)
    yellow  = State('Yellow')
    red  = State('Red')

    # transitions
    slowdown = green.to(yellow)
    stop = yellow.to(red)
    go = red.to(green)

    # parameters
    time_left = 30

    def __init__(self, name):

        super().__init__(name)

    def on_slowdown(self):

        self.time_left = 3

    def on_stop(self):

        self.time_left = 20

    def on_go(self):

        self.time_left = 30

    def while_green(self):

        if self.time_left == 0:

            self.slowdown()

        self.time_left -= 1

    def while_yellow(self):

        if self.time_left == 0:

            self.stop()

        self.time_left -= 1

    def while_red(self):

        if self.time_left == 0:

            self.go()
        
        self.time_left -= 1

    def __str__(self):

        return f"{self.name}: {self.get_state()} - {self.time_left} second left."

traffic_light = hades_app.get_machine('TrafficLight')

@flask_app.route("/")
def hello_world():

    return f"<p>{traffic_light} </p>"


if __name__ == "__main__":

    with PyHadesContext(hades_app):
        
        flask_app.run()
```