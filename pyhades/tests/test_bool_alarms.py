import unittest
from pyhades.alarms import Alarm
from pyhades.alarms.states import AlarmState, States
from pyhades.alarms.trigger import TriggerType
from pyhades.dbmodels import Tags
from pyhades.tests import app


class TestBoolAlarms(unittest.TestCase):

    def setUp(self) -> None:

        self.__tags = [
            ('PT-100', 'Pa', 'float', 'Inlet Pressure', 'PT-100')
        ]

        for name, unit, data_type, description, display_name in self.__tags:

            self._tag = name

            Tags.create(
                name=name,  
                unit=unit, 
                data_type=data_type,
                description=description,
                display_name=display_name)


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
        app.append_alarm(self._alarm)
        return super().setUp()

    def tearDown(self) -> None:

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
