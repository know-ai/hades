# PyHades
A python library to develop continuous tasks using concurrency sync or async

## Installation
You can install PyHades from PyPi
```python
pip install PyHades
```

# Usage
PyHades is based on Singleton Pattern, so you can instantiate it anywhere in your app and it will keep its reference and be the same object throughout your app.

```python
from pyhades import PyHades

app = PyHades()
```

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

## State Machines
You can also create your own classes using the [state machine](https://en.wikipedia.org/wiki/State_pattern#:~:text=The%20state%20pattern%20is%20a,concept%20of%20finite%2Dstate%20machines.) design pattern on a simple way.

```python
from pyhades import PyHades, PyHadesStateMachine, State

app = PyHades()

@app.define_machine('TwoStep', 0.1, mode="async")
class TwoStep(PyHadesStateMachine):

    # states

    state1  = State('State1', initial=True)
    state2  = State('State2')

    # transitions

    forward = state1.to(state2)
    back = state2.to(state1)

    # parameters

    count = 0

    def __init__(self, name):

        super().__init__(name)

    def on_back(self):

        self.count = 0

    def while_state1(self):

        self.count += 1

        print(f"{self.name}: {self.count} - {self.get_state()}")
        if self.count == 5:
            self.forward()

    def while_state2(self):

        self.count += 1

        print(f"{self.name}: {self.count} - {self.get_state()}")
        if self.count >= 10:
            self.back()

if __name__=='__main__':

    app.run()
```