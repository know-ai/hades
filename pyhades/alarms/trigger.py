from enum import Enum

class TriggerType(Enum):

    HH = "HIGH-HIGH"
    H = "HIGH"
    L = "LOW"
    LL = "LOW-LOW"
    B = "BOOL"
    NONE = "NOT DEFINED"


class Trigger:

    def __init__(self):

        self.__type = TriggerType.NONE
        self.__value = None

    @property
    def type(self):
        r"""
        Documentation here
        """

        return self.__type

    @type.setter
    def type(self, _type:str):

        self.__type = TriggerType(_type)

    @property
    def value(self):
        r"""
        Documentation here
        """
        return self.__value

    @value.setter
    def value(self, value):

        if self.type==TriggerType.B:

            if isinstance(value, bool):

                self.__value = value

            else:

                self.__value = bool(value)

        else:

            if isinstance(value, (float, int)):

                self.__value = value