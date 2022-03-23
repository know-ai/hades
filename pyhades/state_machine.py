from email import message
import logging
from inspect import ismethod
from .utils import log_detailed

from statemachine import StateMachine
from statemachine import State as _State


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

    """

    def __init__(self, name, **kwargs):
        
        super(PyHadesStateMachine, self).__init__()
        self.name = name
        self._machine_interval = list()

        attrs = self.get_attributes()

        for key, value in attrs.items():
        
            try:

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
    
    def get_states(self):

        return [state.identifier for state in self.states]

    def get_state_interval(self):
        
        return self.current_state.interval

    def get_interval(self):

        return self._machine_interval

    def set_interval(self, interval):

        self._machine_interval = interval

    @classmethod
    def get_attributes(cls):

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

        result = list()

        current_state = self.current_state

        transitions = self.transitions

        for transition in transitions:

            if transition.source == current_state:

                result.append(transition)

        return result

    def _activate_triggers(self):

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

    def _loop(self):

        try:
            state_name = self.current_state.identifier.lower()
            method_name = "while_" + state_name

            if method_name in dir(self):

                method = getattr(self, method_name)

                # loop machine
                try:
                    method()
                except Exception as e:
                    message = "Machine - {}: Error on machine loop".format(self.name)
                    log_detailed(e, message)

            self._activate_triggers()

        except Exception as e:
            error = str(e)
            logging.error("Machine - {}:{}".format(self.name, error))

    def loop(self):

        self._loop()
    
    def serialize(self):

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

        result["state"] = self.current_state.identifier

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

                except Exception as e:
                    
                    error = str(e)

                    logging.error("Machine - {}:{}".format(self.name, error))
                    value = None

            result[key] = value

        return result

    def get_state(self):
        r"""
        Documentation here
        """

        return self.current_state.identifier
        