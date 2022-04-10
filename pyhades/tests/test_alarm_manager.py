import unittest
from pyhades.alarms import Alarm
from pyhades.alarms.states import AlarmState, States
from pyhades.alarms.trigger import TriggerType
from pyhades import PyHades


class TestAlarmManager(unittest.TestCase):
    r"""
    Documentation here
    """

    def setUp(self) -> None:

        # Init DB
        self.dbfile = "app.db"
        self.app = PyHades()
        self.app.set_mode('Development')
        self.app.drop_db(dbfile=self.dbfile)
        self.app.set_db(dbfile=self.dbfile)
        self.db_worker = self.app.init_db()

        self._alarms = list()
        self._tag_alarms = list()
        # Define Alarms HH - H - B - L - LL
        self.alarm1 = Alarm(name='Alarm-PT-100-HH', tag='PT-100', description='High High Pressure of Tank 100')
        self.alarm1.set_trigger(value=110.0, _type=TriggerType.HH.value)
        self.alarm1.tag_alarm = 'Alarm 1'
        self.app.append_alarm(self.alarm1)
        self._alarms.append(self.alarm1)
        self._tag_alarms.append(self.alarm1.tag_alarm)

        self.alarm2 = Alarm(name='Alarm-PT-100-H', tag='PT-100', description='High Pressure of Tank 100')
        self.alarm2.set_trigger(value=100.0, _type=TriggerType.H.value)
        self.alarm2.tag_alarm = 'Alarm 2'
        self.app.append_alarm(self.alarm2)
        self._alarms.append(self.alarm2)
        self._tag_alarms.append(self.alarm2.tag_alarm)

        self.alarm3 = Alarm(name='Alarm-Surge-C-100', tag='C-100', description='Compressor 100 Surge Alarm')
        self.alarm3.set_trigger(value=True, _type=TriggerType.B.value)
        self.alarm3.tag_alarm = 'Alarm 3'
        self.app.append_alarm(self.alarm3)
        self._alarms.append(self.alarm3)
        self._tag_alarms.append(self.alarm3.tag_alarm)

        self.alarm4 = Alarm(name='Alarm-PT-100-L', tag='PT-100', description='Low Pressure of Tank 100')
        self.alarm4.set_trigger(value=50.0, _type=TriggerType.L.value)
        self.alarm4.tag_alarm = 'Alarm 4'
        self.app.append_alarm(self.alarm4)
        self._alarms.append(self.alarm4)
        self._tag_alarms.append(self.alarm4.tag_alarm)

        self.alarm5 = Alarm(name='Alarm-PT-100-LL', tag='PT-100', description='Low Low Pressure of Tank 100')
        self.alarm5.set_trigger(value=20.0, _type=TriggerType.LL.value)
        self.alarm5.tag_alarm = 'Alarm 5'
        self.app.append_alarm(self.alarm5)
        self._alarms.append(self.alarm5)
        self._tag_alarms.append(self.alarm5.tag_alarm)

        return super().setUp()

    def tearDown(self) -> None:

        # Drop DB
        self.app.stop_db(self.db_worker)
        self.app.drop_db(dbfile=self.dbfile)
        del self.app
        return super().tearDown()

    def testAlarmsAppended(self):

        alarm_manager = self.app.get_alarm_manager()
        summary = alarm_manager.summary()

        self.assertEqual(summary['length'], 5)

    def testGetAlarms(self):

        alarm_manager = self.app.get_alarm_manager()
        alarms = alarm_manager.get_alarms()

        self.assertListEqual(alarms, self._alarms)

    def testGetAlarm(self):

        alarm_manager = self.app.get_alarm_manager()

        alarm_name = 'Alarm-PT-100-HH'
        tag = 'PT-100'
        alarm = alarm_manager.get_alarm(alarm_name)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-PT-100-H'
        tag = 'PT-100'
        alarm = alarm_manager.get_alarm(alarm_name)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-PT-100-L'
        tag = 'PT-100'
        alarm = alarm_manager.get_alarm(alarm_name)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-PT-100-LL'
        tag = 'PT-100'
        alarm = alarm_manager.get_alarm(alarm_name)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-Surge-C-100'
        tag = 'C-100'
        alarm = alarm_manager.get_alarm(alarm_name)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

    def testGetAlarmsByTag(self):

        alarm_manager = self.app.get_alarm_manager()

        tag = 'PT-100'
        alarms = alarm_manager.get_alarms_by_tag(tag)
        with self.subTest(f"Testing alarms associated to tag: {tag}"):
            alarm_names = [alarm.name for alarm in alarms]
            self.assertEqual(alarm_names, ['Alarm-PT-100-HH', 'Alarm-PT-100-H', 'Alarm-PT-100-L', 'Alarm-PT-100-LL'])

        tag = 'C-100'
        alarms = alarm_manager.get_alarms_by_tag(tag)
        with self.subTest(f"Testing alarms associated to tag: {tag}"):
            alarm_names = [alarm.name for alarm in alarms]
            self.assertEqual(alarm_names, ['Alarm-Surge-C-100'])

    def testGetSubscribedTags(self):

        alarm_manager = self.app.get_alarm_manager()

        subscribed_tags = alarm_manager.tags()

        tags = ['PT-100', 'C-100']

        for tag in subscribed_tags:

            with self.subTest(f"Testing tag {tag} associate in alarms"):

                self.assertTrue(tag in tags)

    def testSummary(self):

        alarm_manager = self.app.get_alarm_manager()

        summary = alarm_manager.summary()

        with self.subTest("Testing length in summary"):

            self.assertEqual(summary['length'], 5)

        for count, alarm_name in enumerate(summary['alarms']):

            with self.subTest(f"Testing alarm names in alarm summary"):

                self.assertEqual(alarm_name, self._alarms[count].name)

        with self.subTest("Testing alarm tags in summary"):

            self.assertListEqual(summary['alarm_tags'], self._tag_alarms)

        tags = ['PT-100', 'C-100']

        for tag in summary['tags']:

            with self.subTest(f"Testing tag {tag} associate in alarm summary"):

                self.assertTrue(tag in tags)

    def testSimulateExecuteWorker(self):

        from pyhades.tags import CVTEngine
        tag_engine = CVTEngine()
        tags = [
            ("PT-100", 'kPa', 'float', 'Pressure for Tank 100', 0.0, 200.0),
            ("C-100", 'Adim', 'bool', 'Surge for Compressor 100')
        ]
        tag_engine.set_tags(tags)

        alarm_manager = self.app.get_alarm_manager()

        # Iteration 1 Normal Operation
        tag_engine.write_tag('PT-100', 75.0)
        tag_engine.write_tag('C-100', False)
        for tag, *args in tags:

            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-HH')
        with self.subTest("Testing HIGH-HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-H')
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Surge Alarm
        alarm = alarm_manager.get_alarm('Alarm-Surge-C-100')
        with self.subTest("Testing Surge alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-L')
        with self.subTest("Testing Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Low Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-LL')
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)


        # Iteration 2
        tag_engine.write_tag('PT-100', 102.0)
        tag_engine.write_tag('C-100', False)
        for tag, *args in tags:

            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-HH')
        with self.subTest("Testing HIGH-HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-H')
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## Surge Alarm
        alarm = alarm_manager.get_alarm('Alarm-Surge-C-100')
        with self.subTest("Testing Surge alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-L')
        with self.subTest("Testing Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Low Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-LL')
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        # Iteration 3
        tag_engine.write_tag('PT-100', 112.0)
        tag_engine.write_tag('C-100', False)
        for tag, *args in tags:

            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-HH')
        with self.subTest("Testing HIGH-HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-H')
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## Surge Alarm
        alarm = alarm_manager.get_alarm('Alarm-Surge-C-100')
        with self.subTest("Testing Surge alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-L')
        with self.subTest("Testing Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        ## Low Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-LL')
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)


        # Iteration 4
        tag_engine.write_tag('PT-100', 45.0)
        tag_engine.write_tag('C-100', True)
        for tag, *args in tags:

            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-HH')
        with self.subTest("Testing HIGH-HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.RTNUN.state)

        ## HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-H')
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.RTNUN.state)

        ## Surge Alarm
        alarm = alarm_manager.get_alarm('Alarm-Surge-C-100')
        with self.subTest("Testing Surge alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-L')
        with self.subTest("Testing Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## Low Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-LL')
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.NORM.state)

        # Iteration 5
        tag_engine.write_tag('PT-100', 15.0)
        tag_engine.write_tag('C-100', True)
        for tag, *args in tags:

            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-HH')
        with self.subTest("Testing HIGH-HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.RTNUN.state)

        ## HIGH Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-H')
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.RTNUN.state)

        ## Surge Alarm
        alarm = alarm_manager.get_alarm('Alarm-Surge-C-100')
        with self.subTest("Testing Surge alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-L')
        with self.subTest("Testing Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

        ## Low Low Alarm
        alarm = alarm_manager.get_alarm('Alarm-PT-100-LL')
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertEqual(alarm.state.state, AlarmState.UNACK.state)

if __name__=='__main__':

    unittest.main()