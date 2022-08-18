import logging
from inspect import ismethod
from .utils import log_detailed

from statemachine import StateMachine
from statemachine import State as _State

from .tags import CVTEngine, TagBinding, GroupBinding
from .logger import DataLoggerEngine
from .models import FloatType, IntegerType, BooleanType, StringType

FLOAT = "float"
INTEGER = "int"
BOOL = "bool"
STRING = "str"

READ = "read"
WRITE = "write"

class State(_State):

    """
    Class used to define custom states in a state machine.

    This class is used to define custom states in a state machine.

    **Parameters:**
        
    * **name** (str): state machine name.
    * **interval** (float): machine loop time for this state in seconds.

    Usage:

    ```python
    state1  = State('State1', initial=True)
    state2  = State('State2', interval=0.5)
    """

    def __init__(self, *args, **kwargs):

        super(State, self).__init__(*args, **kwargs)
        self._trigger = None
        
        if "interval" in kwargs:
            self._interval = kwargs["interval"]
        else:
            self._interval = float('inf')

        self._transition = None

    def to(self, another, trigger=None):

        """
        This method allows to create transitions between states,
        you can also define trigger conditions in order to execute
        transitions
        """

        self._transition = super(State, self).to(another)
        self._trigger = trigger

        return self._transition

    @property
    def interval(self):

        return self._interval

    def attach_all(self):

        if not self._trigger:
            return

    
class PyHadesStateMachine(StateMachine):

    """
    Class used to define custom state machines.

    This class is used to define custom machines,
    by defining parameters, states, transitions and 
    by defining methods state behaviour can de defined.

    **Parameters:**
        
    * **name** (str): state machine name.

    **Attributes**

    * **tag_engine** (CVTEngine Object)
    * **logger_engine** (DataLoggerEngine Object) 

    """
    tag_engine = CVTEngine()
    logger_engine = DataLoggerEngine()

    def __init__(self, name:str, **kwargs):
        
        super(PyHadesStateMachine, self).__init__()
        self.name = name
        self._tag_bindings = list()
        self._group_bindings = list()
        self._machine_interval = list()

        attrs = self.get_attributes()

        for key, value in attrs.items():
        
            try:
                if isinstance(value, TagBinding):
                    self._tag_bindings.append((key, value))
                    _value = self.tag_engine.read_tag(value.tag)

                    setattr(self, key, _value)

                if isinstance(value, GroupBinding):
                    self._group_bindings.append((key, value))
                    _value = value.values

                    setattr(self, key, _value)

                if key in kwargs:
                    default = kwargs[key]
                else:
                    default = value.default
                    _type = value._type
                    
                if default:
                    setattr(self, key, default)
                else:
                    if _type == FLOAT:
                        setattr(self, key, 0.0)
                    elif _type == INTEGER:
                        setattr(self, key, 0)
                    elif _type == BOOL:
                        setattr(self, key, False)
                    elif _type == STRING:
                        setattr(self, key, "")
            except Exception as e:
                continue

        self.attrs = attrs

    def info(self)->str:
        r"""
        Gets general information of the state machine

        **Returns**

        * **(str)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> info = machine.info()
        ```
        """
        return f'''\nState Machine: {self.name} - Interval: {self.get_interval()} seconds - States: {self.get_states()} - Transitions: {self.get_transitions_name()}'''
    
    def get_states(self)->list:
        r"""
        Gets a list of state machine's names

        **Returns**

        * **(list)**

        Usage
        
        ```python
        >>> machine = app.get_machine(name)
        >>> states = machine.get_states()
        ```
        """
        return [state.identifier for state in self.states]

    def get_state_interval(self)->float:
        r"""
        Gets current state interval

        **Returns**

        * **(float)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> current_interval = machine.get_state_interval()
        ```

        """
        return self.current_state.interval

    def get_interval(self)->float:
        r"""
        Gets overall state machine interval

        **Returns**

        * **(float)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> interval = machine.get_interval()
        ```
        """
        return self._machine_interval

    def set_interval(self, interval):
        r"""
        Sets overall machine interval

        **Parameters**

        * **interval:** (float) overal machine interval in seconds

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> machine.set_interval(0.5)
        ```
        """
        self._machine_interval = interval

    @classmethod
    def get_attributes(cls):
        r"""
        Gets class attributes defined by [model types]()

        **Returns**

        * **(dict)**
        """
        result = dict()
        
        props = cls.__dict__

        forbidden_attributes = (
            "states", 
            "transitions", 
            "states_map", 
            "_loop", 
            "get_attributes", 
            "_tag_bindings", 
            "_get_active_transitions", 
            "_activate_triggers",
            "get_state_interval",
            "get_interval",
            "set_interval",
            "_machine_interval"
        )

        for key, value in props.items():


            if key in forbidden_attributes:
                continue
            if hasattr(value, '__call__'):
                continue
            if isinstance(value, cls):
                continue
            if isinstance(value, State):
                continue
            if not ismethod(value):

                if not "__" in key:
                    result[key] = value

        return result

    def _get_active_transitions(self):
        r"""
        Gets allowed transitions based on the current state

        **Returns**

        * **(list)**
        """
        result = list()

        current_state = self.current_state

        transitions = self.transitions

        for transition in transitions:

            if transition.source == current_state:

                result.append(transition)

        return result

    def get_transitions_name(self):
        r"""
        Get all transitions name define in the state machine

        **Returns**

        * **(list)** of string
        """
        transitions = self.transitions
        
        _transitions = list()

        for transition in transitions:
            _transitions.append(transition.identifier)

        return _transitions

    def _activate_triggers(self):
        r"""
        Allows to execute the on_ method in transitions when it's necesary

        """
        transitions = self._get_active_transitions()

        for transition in transitions:
            method_name = transition.identifier
            method = getattr(self, method_name)

            try:
                source = transition.source
                if not source._trigger:
                    continue
                if source._trigger.evaluate():
                    method()
            except Exception as e:
                error = str(e)
                logging.error("Machine - {}:{}".format(self.name, error))

    def _update_tags(self, direction=READ):

        for attr, _binding in self._tag_bindings:

            try:
                if direction == READ and _binding.direction == READ:
                
                    tag = _binding.tag
                    value = self.tag_engine.read_tag(tag)
                    value = setattr(self, attr, value)
                
                elif direction == WRITE and _binding.direction == WRITE:
                    tag = _binding.tag
                    value = getattr(self, attr)
                    self.tag_engine.write_tag(tag, value)
            
            except Exception as e:
                message = "Machine - {}: Error on machine tag-bindings".format(self.name)
                log_detailed(e, message)

    def _update_groups(self, direction=READ):
    
        for attr, _binding in self._group_bindings:

            try:
                if direction == READ and _binding.direction == READ:
                
                    _binding.update()

                    setattr(self, attr, _binding.values)
                
                elif direction == WRITE and _binding.direction == WRITE:
                    
                    values = getattr(self, attr)
                    
                    _binding.values = values

                    _binding.update()
            
            except Exception as e:
                message = "Machine - {}: Error on machine group-bindings".format(self.name)
                log_detailed(e, message)

    def _loop(self):
        r"""
        Documentation in construction
        """
        try:
            state_name = self.current_state.identifier.lower()
            method_name = "while_" + state_name

            if method_name in dir(self):
                update_tags = getattr(self, '_update_tags')
                update_groups = getattr(self, '_update_groups')
                method = getattr(self, method_name)

                # update tag read bindings
                update_tags()
                update_groups()

                # loop machine
                try:
                    method()
                except Exception as e:
                    message = "Machine - {}: Error on machine loop".format(self.name)
                    log_detailed(e, message)

                #update tag write bindings
                update_tags("write")
                update_groups("write")

            self._activate_triggers()

        except Exception as e:
            error = str(e)
            logging.error("Machine - {}:{}".format(self.name, error))

    def loop(self):
        r"""
        Starts state machine thread and it allows to execute the correct while_ method
        in the state machine loop execution
        """
        self._loop()
    
    def serialize(self)->dict:
        r"""
        Gets state machine attributes serialized
        """
        def is_serializable(value):

            if isinstance(value, float):
                return True

            if isinstance(value, int):
                return True

            if isinstance(value, bool):
                return True

            if isinstance(value, str):
                return True

            return False

        def ismodel_instance(obj):

            for cls in [FloatType, IntegerType, BooleanType, StringType]:
                if isinstance(obj, cls):
                    return True
            return False

        result = dict()

        result["name"] = {
            'value': self.name,
            'unit': None
        }

        result["state"] = {
            'value': self.current_state.identifier,
            'unit': None
        }

        states = self.get_states()
        checkers = ["is_" + state for state in states]
        methods = ["while_" + state for state in states]

        attrs = self.get_attributes()
        
        for key in attrs.keys():
            
            if key in checkers:
                continue
            if key in methods:
                continue
            if not ismodel_instance(attrs[key]):
                continue

            obj = attrs[key]
            unit = obj.unit
            value = getattr(self, key)

            if not is_serializable(value):
                try:
                    obj = attrs[key]

                    if isinstance(obj, FloatType):
                        value = float(value)
                    elif isinstance(obj, IntegerType):
                        value = int(value)
                    elif isinstance(obj, BooleanType):
                        value = bool(value)
                    else:
                        value = str(value)
                    
                    unit = obj.unit

                except Exception as e:
                    
                    error = str(e)

                    logging.error("Machine - {}:{}".format(self.name, error))
                    value = None

            result[key] = {
                'value': value,
                'unit': unit
            }

        return result

    def get_state(self):
        r"""
        Gets current state of the state machine

        **Returns**

        * **state:** (str) current state of the state machine
        """

        return self.current_state.identifier
        