from enum import Enum


class States(Enum):

    NORM = "Normal"
    UNACK = "Unacknowledged"
    ACKED = "Acknowledged"
    RTNUN = "RTN Unacknowledged"
    SHLVD = "Shelved"
    DSUPR = "Suppressed By Design"
    OOSRV = "Out Of Service"


class Status(Enum):

    ACTV = "Active"
    NACTV = "Not Active"
    ANNCTD = "Annunciated"
    NANNCTD = "Not Annunciated"
    OR = "Not Active or Active"
    SUPR = "Suppressed"
    NA = "Not Applicable"
    NORM = "Normal"
    ABNORM = "Abnormal"


class AlarmAttrs:

    def __init__(
        self, 
        mnemonic: str, 
        state: str, 
        process_condition: str,
        is_triggered: bool, 
        alarm_status: str, 
        annunciate_status: str, 
        acknowledge_status: str,
        audible: bool, 
        color: bool, 
        symbol: bool, 
        blinking: bool
    ):
        self.__mnemonic = mnemonic
        self.__state = state
        self.__process_condition = process_condition
        self.__alarm_status = alarm_status
        self.__annunciate_status = annunciate_status
        self.__acknowledge_status = acknowledge_status
        self.__is_triggered = is_triggered
        self.__audible = audible
        self.__color = color
        self.__symbol = symbol
        self.__blinking = blinking

    @property
    def mnemonic(self):
        r"""
        Documentation here
        """
        return self.__mnemonic

    @property
    def state(self):
        r"""
        Documentation here
        """
        return self.__state
    
    @property
    def process_condition(self):
        r"""
        Documentation here
        """
        return self.__process_condition

    @property
    def alarm_status(self):
        r"""
        Documentation here
        """
        return self.__alarm_status

    @property
    def is_triggered(self):
        r"""
        Documentation here
        """
        return self.__is_triggered

    @property
    def annunciate_status(self):
        r"""
        Documentation here
        """
        return self.__annunciate_status

    @property
    def acknowledge_status(self):
        r"""
        Documentation here
        """
        return self.__acknowledge_status

    @property
    def audible(self):
        r"""
        Documentation here
        """
        return self.__audible

    def silence(self):
        r"""
        Documentation here
        """
        self.__audible = False

    def return_to_audible(self):
        r"""
        Documentation here
        """
        self.__audible = True

    @property
    def color(self):
        r"""
        Documentation here
        """
        return self.__color

    @property
    def symbol(self):

        return self.__symbol

    @property
    def blinking(self):
        r"""
        Documentation here
        """
        return self.__blinking

    def is_acknowledged(self):
        r"""
        Documentation here
        """

        return self.acknowledge_status == States.ACKED.value

    def serialize(self):
        r"""
        Documentation here
        """
        return {
            'mnemonic': self.mnemonic,
            'state': self.state,
            'process_condition': self.process_condition,
            'alarm_status': self.alarm_status,
            'is_triggered': self.is_triggered,
            'annunciate_status': self.annunciate_status,
            'acknowledge_status': self.acknowledge_status,
            'audible': self.audible,
            'color': self.color,
            'symbol': self.symbol,
            'blinking': self.blinking
        }


class AlarmState:

    NORM = AlarmAttrs(
        mnemonic=States.NORM.name,
        state=States.NORM.value,
        process_condition=Status.NORM.value,
        alarm_status=Status.NACTV.value,
        is_triggered=False,
        annunciate_status=Status.NANNCTD.value,
        acknowledge_status=States.ACKED.value,
        audible=False,
        color=False,
        symbol=False,
        blinking=False
    )
    UNACK = AlarmAttrs(
        mnemonic=States.UNACK.name,
        state=States.UNACK.value,
        process_condition=Status.ABNORM.value,
        alarm_status=Status.ACTV.value,
        is_triggered=True,
        annunciate_status=Status.ANNCTD.value,
        acknowledge_status=States.UNACK.value,
        audible=True,
        color=True,
        symbol=True,
        blinking=True
    )
    ACKED = AlarmAttrs(
        mnemonic=States.ACKED.name,
        state=States.ACKED.value,
        process_condition=Status.ABNORM.value,
        alarm_status=Status.ACTV.value,
        is_triggered=True,
        annunciate_status=Status.ANNCTD.value,
        acknowledge_status=States.ACKED.value,
        audible=False,
        color=True,
        symbol=True,
        blinking=False
    )
    RTNUN = AlarmAttrs(
        mnemonic=States.RTNUN.name,
        state=States.RTNUN.value,
        process_condition=Status.NORM.value,
        alarm_status=Status.NACTV.value,
        is_triggered=False,
        annunciate_status=Status.ANNCTD.value,
        acknowledge_status=States.UNACK.value,
        audible=False,
        color=True,
        symbol=True,
        blinking=False
    )
    SHLVD = AlarmAttrs(
        mnemonic=States.SHLVD.name,
        state=States.SHLVD.value,
        process_condition=Status.NORM.value,
        alarm_status=Status.OR.value,
        is_triggered=False,
        annunciate_status=Status.SUPR.value,
        acknowledge_status=Status.NA.value,
        audible=False,
        color=False,
        symbol=True,
        blinking=False
    )
    DSUPR = AlarmAttrs(
        mnemonic=States.DSUPR.name,
        state=States.DSUPR.value,
        process_condition=Status.NORM.value,
        alarm_status=Status.OR.value,
        is_triggered=False,
        annunciate_status=Status.SUPR.value,
        acknowledge_status=Status.NA.value,
        audible=False,
        color=False,
        symbol=True,
        blinking=False
    )
    OOSRV = AlarmAttrs(
        mnemonic=States.OOSRV.name,
        state=States.OOSRV.value,
        process_condition=Status.NORM.value,
        alarm_status=Status.OR.value,
        is_triggered=False,
        annunciate_status=Status.SUPR.value,
        acknowledge_status=Status.NA.value,
        audible=False,
        color=False,
        symbol=True,
        blinking=False
    )

    _states = [NORM, UNACK, ACKED, RTNUN, SHLVD, DSUPR, OOSRV]

    @classmethod
    def get_state_by_name(cls, state:str):
        r"""
        Documentation here
        """
        _state = States(state)

        for alarm_state in cls._states:

            if _state==alarm_state:

                return alarm_state

