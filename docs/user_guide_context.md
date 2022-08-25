# Context Manager with PyHades
When you need to run hades threads integrated with web services that have a main thread, you must run the application that contains the main thread inside a PyHades Context and pass the PyHades application object to this context.

## [Flask](https://flask.palletsprojects.com/en/2.0.x/) Integration
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