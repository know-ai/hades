# Current Value Table (CVT)

Whatever app that you want to do in the process industry is necessary to get the process variables from industrial protocols like Classic OPC - OPC UA - Modbus among others protocols, and share them around whole the app to use them.

Here is where the CVT and CVTEngine Classes play a fundamental role.

CVTEngine is like a tags repository based on Singleton pattern that allows to you share the variables through the app using a robust OPC UA data structure.

This means that regardless of the way you obtain the field variables, within the application it will be handled under the OPC UA standard and structure.

This will help you to have a data structure for the process variables very well referenced within the application. Also, due to the multi-threaded nature of PyHades, CVT allows you to distribute data in your application in a safe way without interfering with the threads executed by PyHades.

In short, you can define objects in your app that represents field variables called Tags, these objects have a number of attributes that allows you to know all the necessary information of a field variable.

Usage

```python
>>> from pyhades.tags import CVTEngine
>>> tag_engine = CVTEngine()
```

## Defining Tags

A tag is an object representation of field measurement or a field device, for this reason, you must pass son attributes in a tuple form to the *set_tag* method of CVTEngine instance.

So, the necessary attributes are:

- name: **(str)** Tag name with which the object will be saved in the CVTEngine repository
- unit: **(str)** Measurement unit of the field variable
- data_type: **(str)** Data type of the field variable ['float', 'int', 'bool', 'str']
- description: **(str)** Field variable description
- min_value: **(float)[optional]** Lower range of the field instrument.
- max_value: **(float)[optional]** Higher range of the field instrument.
- tcp_source_address: **(str)[optional]** Url for tcp communication with a server.
- node_namespace: **(str)[Optional]** Node ID or Namespace (OPC UA) to get element value from server.
 
Usage

```python
>>> tag_engine.set_tag('TAG1', 'ºC', 'float', 'Inlet temprerature', 0.0, 100.0, 'opc.tcp://localhost:53530/OPCUA/SimulationServer', 'ns=3;i=1001')
```

It is important to respect the order of the variables.

It is also required to enter the name, unit and data type as minimum requirements.

You can also define a list of tags in the repository.

```python
>>> tags = [
        ("TAG1", 'ºC', 'float', 'Inlet temperature', 0.0, 100.0),
        ("TAG2", 'kPa', 'float', 'Inlet pressure', 100.0),
        ("TAG3", 'm3/s', 'float', 'Inlet flow')
    ]
>>> tag_engine.set_tags(tags)
```

On the other hand, if you want to group certain variables according to your criteria, you can do it using *set_group* method.

```python
>>> temp_tags = [
        ("TAG1", 'ºC', 'float', 'Inlet temperature', 0.0, 100.0),
        ("TAG2", 'ºC', 'float', 'Outlet temperature', 0.0, 100.0)
    ]
>>> pressure_tags = [
        ("TAG3", 'kPa', 'float', 'Inlet pressure', 100.0, 200.0),
        ("TAG4", 'kPa', 'float', 'Outlet pressure', 0.0, 100.0)
    ]
>>> tag_engine.set_group('Temperatures', temp_tags)
>>> tag_engine.set_group('Pressures', pressure_tags)
```

In this way, in another part of the application you can obtain the tag names that are part of a specific group

```python
>>> tag_engine.get_group('Temperatures')
['TAG1', 'TAG2']
>>> tag_engine.get_group('Pressures')
['TAG3', 'TAG4']
```

**Note:** If you want to define a tag with a unit different from those defined, you can define new variables and units, see the [database model](dbmodels.md) section

## Unit Conversions

Tags represent process variables, these tags have attributes, inside these attributes we have *unit*, it represents the tag's unit.

For example, a tag can represent the pressure in a tank, so, this variable can be of different unit *250 kPa*.

So, you can define different multiplier for unit conversions according [the International Society of Automation, ISA](https://www.isa.org/getmedia/192f7bda-c77c-480a-8925-1a39787ed098/CCST-Conversions-document.pdf) standard, preferable.

Currently, PyHades offers some conversions by default, according to variables and units defined. see the [database model](dbmodels.md) section.

If you want to add new conversions factor, you must define a json file with the following structure:

```json
{
    "unit_name_1": {
        "unit_name_2": factor_value
    }
}
```

*factor_value* is the multiplier to convert *unit_name_1* to *unit_name_2*

For example:


```json
{
    "meters": {
        "inches": 39.37008
    },
    "meter_cube": {
        "liter": 1000
    }
}
```

The example above define that 1 meters = 39.37008 inches, and 1 meter_cube = 1000 liter.

**NOTE:** It's important that *unit_name* must be defined into dbmodel as it explained in [database model](dbmodels.md) section

Once you define the json file, you can load it into the application with CVTEngine:

```pythonn
from pyhades.tags import CVTEngine

tag_engine = CVTEngine()
tag_engine.add_conversions("root_path/units.json")
```

## Write and Read Values to the CVTEngine repository

Once you have defined all your tags, the other important step is to write and read values to and from the CVTEngine repository with a safe-thread mechanism.

### Write values

```python
>>> tag_engine.write_tag('TAG1', 50.53)
```

### Read values

```python
>>> tag_engine.read_tag('TAG1')
50.53
```
You can also read tag value with another unit.

```python
>>> tag_engine.read_tag('TAG1', unit='K')
323.68
```

## Read attributes from CVTEngine repository

Sometimes you will need to read the attributes contained in the data structure of a previously configured tag.

```python
>>> tag_engine.read_attributes('TAG1')
{
    "value":{
            "status_code":{
            "name": 'GOOD',
            "value": '0x000000000',
            "description":  'Operation succeeded'
        },
        "source_timestamp": '03/25/2022, 14:39:29.189422',
        "value": 50.53,
    },
    'name': 'TAG1', 
    'unit': 'ºC', 
    'data_type': 'float', 
    'description': 'Inlet temperature', 
    'min_value': 0.0, 
    'max_value': 100.0
}
```

# Tag Binding In State Machines

At the development level, it is more comfortable and less verbose to write and read a variable to the repository in the natural way that a variable is defined in the programming language.

This is where the link between a CVTEngine tag and a programming variable comes into play.

It is necessary to keep in minds that each variable that is binded to the CVTEngine must be defined if it is read or written.

```python
>>> time_left = TagBinding('time_left')
>>> time_left_write = TagBinding('time_left', direction='write')
```

Let's go back to the traffic light example


```python
from pyhades import PyHades, PyHadesStateMachine, State
from pyhades.tags import CVTEngine, TagBinding

app = PyHades()

tag_engine = CVTEngine()
tag_engine.set_tag("time_left", 'seconds', 'int', 'Time left to change traffic light', 0, 30)


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
    time_left = TagBinding('time_left')
    time_left_write = TagBinding('time_left', direction='write')

    def __init__(self, name):
        
        super().__init__(name)
        
    def on_slowdown(self):

        self.time_left_write = 3

    def on_stop(self):

        self.time_left_write = 20

    def on_go(self):

        self.time_left_write = 30

    def while_green(self):

        print(self)
        if self.time_left == 0:
            self.slowdown()
        else:
            self.time_left_write = self.time_left - 1

    def while_yellow(self):

        print(self)
        if self.time_left == 0:
            self.stop()
        else:
            self.time_left_write = self.time_left - 1

    def while_red(self):

        print(self)
        if self.time_left == 0:
            self.go()
        else:
            self.time_left_write = self.time_left - 1

    def __str__(self):

        return f"{self.name}: {self.get_state()} - {self.time_left} second left."

if __name__=='__main__':

    app.run()
```

Note that in the class attributes section the variables that will be linked to the CVTEngine are defined.

You say, why complicate things if according to the zen of python there is a phrase that simple is better than complicated?

Well, it turns out that by inheriting CVTEngine from the singleton design pattern, all fully structured information can be shared throughout the entire application and used throughout the development as if it were a simple variable in the application and also using a thread-safe mechanism.