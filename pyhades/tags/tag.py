from .tag_value import TagValue
from ..utils import Observer

DATETIME_FORMAT = "%m/%d/%Y, %H:%M:%S.%f"

class Tag:

    def __init__(
        self, 
        name, 
        unit, 
        data_type, 
        description="", 
        min_value=None, 
        max_value=None, 
        tcp_source_address=None, 
        node_namespace=None
        ):

        self.name = name
        self.value = TagValue(min_value=min_value, max_value=max_value)
        self.data_type = data_type
        self.description = description
        self._observers = set()
        self.tcp_source_address = tcp_source_address
        self.node_namespace = node_namespace
        self.unit = unit

    def set_value(self, value):

        self.value.update(value)
        self.notify()

    def set_min_value(self, value):

        self.value.set_min_value(value)

    def set_max_value(self, value):

        self.value.set_max_value(value)

    def set_tcp_source_address(self, tcp_source_address):

        self.tcp_source_address = tcp_source_address

    def set_node_namespace(self, node_namespace):

        self.node_namespace = node_namespace
    
    def get_value(self, unit:str=None):
        
        value = self.value.get_value()

        if unit is None:
            
            return value

        raise KeyError(f"{unit} not found")

    def get_value_attributes(self):

        return {
            "status_code":{
                "name": self.value.get_status_code().name,
                "value": self.value.get_status_code().value[0],
                "description":  self.value.get_status_code().value[1]
            },
            "source_timestamp": self.value.get_source_timestamp().strftime(DATETIME_FORMAT),
            "value": self.value.get_value(),
        }

    def get_min_value(self):

        return self.value.get_min_value()

    def get_max_value(self):

        return self.value.get_max_value()

    def get_data_type(self):
        
        return self.data_type

    def get_unit(self):

        return self.unit

    def get_description(self):

        return self.description

    def get_tcp_source_address(self):
        
        return self.tcp_source_address

    def get_node_namespace(self):

        return self.node_namespace

    def get_attributes(self):

        return {
            "value": self.get_value_attributes(),
            "name": self.name,
            "unit": self.get_unit(),
            "data_type": self.get_data_type(),
            "description": self.get_description(),
            "min_value": self.get_min_value(),
            "max_value": self.get_max_value(),
            "tcp_source_address": self.get_tcp_source_address(),
            "node_namespace": self.get_node_namespace()
        }
    
    def attach(self, observer):

        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):

        observer._subject = None
        self._observers.discard(observer)

    def notify(self):

        for observer in self._observers:

            observer.update()

    def parser(self):
        r"""
        Documentation here
        """
        return (
            self.name,
            self.get_unit(),
            self.get_data_type(),
            self.get_description(),
            self.value.get_min_value(),
            self.value.get_max_value(),
            self.get_tcp_source_address(),
            self.get_node_namespace()
        )

    def update(self, **kwargs):
        r"""
        Documentation here
        """

        for key, value in kwargs.items():

            if key in ['max_value', 'min_value']:

                setattr(self.value, key, value)
            
            else:

                setattr(self, key, value)

    def add_custom_conversions(self, custom_conversions_path:str):
        r"""
        Documentation here
        """
        self.__unit_converter.add_custom_conversions(custom_conversions_path)


class TagObserver(Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the subject's.
    Store state that should stay consistent with the subject's.
    """
    def __init__(self, tag_queue):

        super(TagObserver, self).__init__()
        self._tag_queue = tag_queue

    def update(self):

        """
        This methods inserts the changing Tag into a 
        Producer-Consumer Queue Design Pattern
        """
        
        result = dict()

        result["tag"] = self._subject.name
        result["value"] = self._subject.value

        self._tag_queue.put(result)
