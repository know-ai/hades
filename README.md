# PyHades
A python library to develop continuous tasks using concurrency sync or async

___
## Installation
You can install PyHades from PyPi
```python
pip install PyHades
```
___
# Usage
PyHades is based on Singleton Pattern, so you can instantiate it anywhere in your app and it will keep its reference and be the same object throughout your app.

```python
from pyhades import PyHades

app = PyHades()
```
___
## Making Threads
PyHades uses [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor), so, you can define communication threads asynchronously easily using the *thread* decorator.

```python
from pyhades import PyHades

app = PyHades()

@app.thread(period=0.5)
def say_hi():

    print('Hi with 0.5s period')

@app.thread
def say_hello():

    print('Hello with 1s period')
```

## Running Threads
Finally, to run your threads, you must call the *run* method of your app.

```python
app.run()
```
___
## OPCUA Client Threads
You can also evaluate the number of tags you can query an OPC UA server based on the time period you use executing the thread.

This example is based on the library [opcua](https://pypi.org/project/opcua/)

```python
from opcua import Client
from opcua.ua.uatypes import NodeId
from pyhades import PyHades

app = PyHades()

prosys_server = 'opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer'
opcua_client = Client(prosys_server)
opcua_client.connect()
node_ids = ['ns=3;i=1001', 'ns=3;i=1002', 'ns=3;i=1003', 'ns=3;i=1004', 'ns=3;i=1005', 'ns=3;i=1006']

@app.thread(period=0.1)
def get_node_id_value():
    r"""
    Documentation here
    """
    result = list()
    for node_id in node_ids:
        _node = opcua_client.get_node(NodeId.from_string(node_id))
        value = _node.get_value()
        result.append(value)

    print(result)

if __name__=='__main__':

    app.run()
```
___
## State Machines
You can also create your own classes using the [state machine](https://en.wikipedia.org/wiki/State_pattern#:~:text=The%20state%20pattern%20is%20a,concept%20of%20finite%2Dstate%20machines.) design pattern on a simple way.

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
___
## Source code

You can check the latest sources on [GitHub](https://github.com/know-ai/hades):

___
## Documentation

The official documentation can be found in [Read the Docs](https://pyhades.readthedocs.io/en/latest/)