import unittest
from pyhades.alarms import Alarm
from pyhades.alarms.states import AlarmState, States
from pyhades.alarms.trigger import TriggerType
from pyhades import PyHades
from pyhades.dbmodels import Tags, Variables, Units, DataTypes
from datetime import datetime


class TestBoolAlarms(unittest.TestCase):

    def setUp(self) -> None:

        # Init DB
        self.dbfile = "app.db"
        self.app = PyHades()
        self.app.set_mode('Development')
        self.app.drop_db(dbfile=self.dbfile)
        self.app.set_db(dbfile=self.dbfile)
        self.db_worker = self.app.init_db()

        self.__variables = [
            'Pressure',
            'Temperature',
            'Mass_Flow'
        ]

        self.__units = [
            ('Pa', 'Pressure'),
            ('Celsius', 'Temperature'),
            ('kg/s', 'Mass_Flow')
        ]

        self.__data_types = [
            'float',
            'int',
            'str',
            'bool'
        ]

        self.__tags = [
            ('PT-100', 'Pa', 'float', 'Inlet Pressure')
        ]

        for variable_name in self.__variables:

            Variables.create(name=variable_name)

        for name, variable in self.__units:

            Units.create(name=name, variable=variable)

        for datatype_name in self.__data_types:

            DataTypes.create(name=datatype_name)

        for name, unit, data_type, description in self.__tags:

            self._tag = name

            Tags.create(
                name=name,  
                unit=unit, 
                data_type=data_type,
                description=description)


        # Default Alarm
        self._name = "Default Alarm"
        
        self._description = "Default Alarm for Pressure Transmissor 100"

        self._alarm = Alarm(
            name=self._name,
            tag=self._tag,
            description=self._description
        )
        self.trigger_type = TriggerType.B.value
        self.trigger_value = True
        self._alarm.set_trigger(self.trigger_value, self.trigger_type)
        return super().setUp()

    def tearDown(self) -> None:

        # Drop DB
        self.app.stop_db(self.db_worker)
        self.app.drop_db(dbfile=self.dbfile)
        return super().tearDown()
    
    def testAlarmClassType(self):
        
        self.assertIsInstance(self._alarm, Alarm)

    def testCheckAlarmName(self):

        self.assertEqual(self._alarm.name, self._name)

    def testCheckTagBinded(self):

        self.assertEqual(self._alarm.tag, self._tag)

    def testCheckAlarmDescription(self):

        self.assertEqual(self._alarm.description, self._description)

    def testCheckAlarmTag(self):

        alarm_tag = "A-100"
        self._alarm.tag_alarm = alarm_tag
        self.assertEqual(self._alarm.tag_alarm, alarm_tag)

    def testAlarmInitialState(self):
        
        self.assertEqual(self._alarm.state.state, States.NORM.value)

    def testTrigger(self):

        with self.subTest("Testing trigger type in alarms"):

            self.assertEqual(self._alarm._trigger.type.value, self.trigger_type)

        with self.subTest("Testing trigger value in alarms"):

            self.assertEqual(self._alarm._trigger.value, self.trigger_value)

    def testTriggerAlarm(self):

        self._alarm.update(True)
        self.assertEqual(self._alarm.state.state, AlarmState.UNACK.state)

    def testAcknowledgeAlarm(self):

        self._alarm.update(True)
        self._alarm.acknowledge()
        self.assertEqual(self._alarm.state.state, AlarmState.ACKED.state)

    def testRTNUnacknowledgeAlarm(self):

        self._alarm.update(True)
        self._alarm.update(False)
        self.assertEqual(self._alarm.state.state, AlarmState.RTNUN.state)

    def testShelvedAlarm(self):

        seconds = 10
        self._alarm.shelve(seconds=seconds)

        with self.subTest("Testing shelve alarm"):

            self.assertEqual(self._alarm.state.state, AlarmState.SHLVD.state)

        self._alarm.unshelve()

        with self.subTest("Testing unshelve alarm"):

            self.assertEqual(self._alarm.state.state, AlarmState.NORM.state)

    def testSuppressedAlarm(self):

        self._alarm.suppress_by_design()

        with self.subTest("Testing suppress alarm"):

            self.assertEqual(self._alarm.state.state, AlarmState.DSUPR.state)

        self._alarm.unsuppress_by_design()

        with self.subTest("Testing unsuppress alarm"):

            self.assertEqual(self._alarm.state.state, AlarmState.NORM.state)

    def testOutOfServiceAlarm(self):

        self._alarm.out_of_service()

        with self.subTest("Testing out of service alarm"):

            self.assertEqual(self._alarm.state.state, AlarmState.OOSRV.state)

        self._alarm.return_to_service()
        
        with self.subTest("Testing return to service alarm"):

            self.assertEqual(self._alarm.state.state, AlarmState.NORM.state)

if __name__=='__main__':

    unittest.main()