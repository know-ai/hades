from ..status_codes import StatusCode
from datetime import datetime

class TagValue:

    """
    Implement an abstract TagValue Class
    """

    def __init__(self, value=0, min_value=None, max_value=None, source_timestamp:datetime=datetime.now()):

        self.value = value

        self.status_code = StatusCode.GOOD

        self.source_timestamp = source_timestamp

        self.min_value = min_value

        self.max_value = max_value

    def get_value(self):

        return self.value

    def get_source_timestamp(self):

        return self.source_timestamp

    def get_status_code(self):

        return self.status_code
        
    def update(self, value):
        r"""
        Documentation here
        """

        self.value = value

        self.source_timestamp = datetime.now()

        self.status_code = StatusCode.GOOD
        
    def set_min_value(self, min_value):

        self.min_value = min_value

    def get_min_value(self):

        return self.min_value

    def set_max_value(self, max_value):

        self.max_value = max_value

    def get_max_value(self):

        return self.max_value