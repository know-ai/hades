import unittest
from pyhades.alarms import Alarm
from pyhades.dbmodels import Tags, AlarmsDB
from pyhades.alarms.trigger import TriggerType
from pyhades.tests import app, tag_engine


class TestAlarmManager(unittest.TestCase):
    r"""
    Documentation here
    """

    def setUp(self) -> None:

        self.__tags = [
            ('PT-100', 'Pa', 'float', 'Inlet Pressure'),
            ('C-100', 'kg/s', 'float', 'Compressor 100')
        ]
        tag_engine.set_tags(self.__tags)

        for name, unit, data_type, description in self.__tags:

            self._tag = name

            Tags.create(
                name=name, 
                unit=unit, 
                data_type=data_type,
                description=description)

        self._alarms = dict()
        self._tag_alarms = list()
        # Define Alarms HH - H - B - L - LL
        self.alarm1 = Alarm(name='Alarm-PT-100-HH', tag='PT-100', description='High High Pressure of Tank 100')
        self.alarm1.set_trigger(value=110.0, _type=TriggerType.HH.value)
        self.alarm1.tag_alarm = 'Alarm 1'
        app.append_alarm(self.alarm1)
        self._alarms.update({
            '1': self.alarm1
        })
        self._tag_alarms.append(self.alarm1.tag_alarm)

        self.alarm2 = Alarm(name='Alarm-PT-100-H', tag='PT-100', description='High Pressure of Tank 100')
        self.alarm2.set_trigger(value=100.0, _type=TriggerType.H.value)
        self.alarm2.tag_alarm = 'Alarm 2'
        app.append_alarm(self.alarm2)
        self._alarms.update({
            '2': self.alarm2
        })
        self._tag_alarms.append(self.alarm2.tag_alarm)

        self.alarm3 = Alarm(name='Alarm-Surge-C-100', tag='C-100', description='Compressor 100 Surge Alarm')
        self.alarm3.set_trigger(value=True, _type=TriggerType.B.value)
        self.alarm3.tag_alarm = 'Alarm 3'
        app.append_alarm(self.alarm3)
        self._alarms.update({
            '3': self.alarm3
        })
        self._tag_alarms.append(self.alarm3.tag_alarm)

        self.alarm4 = Alarm(name='Alarm-PT-100-L', tag='PT-100', description='Low Pressure of Tank 100')
        self.alarm4.set_trigger(value=50.0, _type=TriggerType.L.value)
        self.alarm4.tag_alarm = 'Alarm 4'
        app.append_alarm(self.alarm4)
        self._alarms.update({
            '4': self.alarm4
        })
        self._tag_alarms.append(self.alarm4.tag_alarm)

        self.alarm5 = Alarm(name='Alarm-PT-100-LL', tag='PT-100', description='Low Low Pressure of Tank 100')
        self.alarm5.set_trigger(value=20.0, _type=TriggerType.LL.value)
        self.alarm5.tag_alarm = 'Alarm 5'
        app.append_alarm(self.alarm5)
        self._alarms.update({
            '5': self.alarm5
        })
        self._tag_alarms.append(self.alarm5.tag_alarm)

        return super().setUp()

    def tearDown(self) -> None:

        return super().tearDown()

    def testAlarmsAppended(self):

        alarm_manager = app.get_alarm_manager()
        summary = alarm_manager.summary()

        self.assertEqual(summary['length'], 5)

    def testGetAlarm(self):

        alarm_manager = app.get_alarm_manager()

        alarm_name = 'Alarm-PT-100-HH'
        tag = 'PT-100'
        _alarm = AlarmsDB.read_by_name(alarm_name)
        alarm = alarm_manager.get_alarm(_alarm.id)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-PT-100-H'
        tag = 'PT-100'
        _alarm = AlarmsDB.read_by_name(alarm_name)
        alarm = alarm_manager.get_alarm(_alarm.id)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-PT-100-L'
        tag = 'PT-100'
        _alarm = AlarmsDB.read_by_name(alarm_name)
        alarm = alarm_manager.get_alarm(_alarm.id)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-PT-100-LL'
        tag = 'PT-100'
        _alarm = AlarmsDB.read_by_name(alarm_name)
        alarm = alarm_manager.get_alarm(_alarm.id)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

        alarm_name = 'Alarm-Surge-C-100'
        tag = 'C-100'
        _alarm = AlarmsDB.read_by_name(alarm_name)
        alarm = alarm_manager.get_alarm(_alarm.id)
        with self.subTest(f"Testing alarm name {alarm_name}"):
            self.assertEqual(alarm.name, alarm_name)

        with self.subTest(f"Testing associated tag {alarm_name}"):
            self.assertEqual(alarm.tag, tag)

    def testGetAlarmsByTag(self):

        alarm_manager = app.get_alarm_manager()

        tag = 'C-100'
        alarms = alarm_manager.get_alarms_by_tag(tag)
        with self.subTest(f"Testing alarms associated to tag: {tag}"):
            alarm_names = [alarm.name for id, alarm in alarms.items()]
            self.assertEqual(alarm_names, ['Alarm-Surge-C-100'])

    def testGetSubscribedTags(self):

        alarm_manager = app.get_alarm_manager()

        subscribed_tags = alarm_manager.tags()

        tags = ['PT-100', 'C-100']

        for tag in subscribed_tags:

            with self.subTest(f"Testing tag {tag} associate in alarms"):

                self.assertTrue(tag in tags)

    def testSummary(self):

        alarm_manager = app.get_alarm_manager()

        summary = alarm_manager.summary()

        tags = ['PT-100', 'C-100']

        for tag in summary['tags']:

            with self.subTest(f"Testing tag {tag} associate in alarm summary"):

                self.assertTrue(tag in tags)

    def testSimulateExecuteWorker(self):

        alarm_manager = app.get_alarm_manager()

        # Iteration 1 Normal Operation
        value = 75.0
        surge_value = False
        tag_engine.write_tag('PT-100', value)
        tag_engine.write_tag('C-100', surge_value)
        for tag, *args in self.__tags:
            
            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-HH')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing HIGH-HIGH alarm state"):
            self.assertIsNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Normal')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-HH')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'NORM')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Normal')
            self.assertEqual(alarm['triggered'], False)
            self.assertEqual(alarm['acknowledged'], True)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'HIGH-HIGH')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'not active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'active', 
                'suppress by design': 'active', 
                'unsuppressed': 'not active', 
                'out of service': 'active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertDictEqual(alarm['operations'], expected_operations)

        ## HIGH Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-H')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertIsNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Normal')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-H')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'NORM')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Normal')
            self.assertEqual(alarm['triggered'], False)
            self.assertEqual(alarm['acknowledged'], True)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'HIGH')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'not active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'active', 
                'suppress by design': 'active', 
                'unsuppressed': 'not active', 
                'out of service': 'active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertDictEqual(alarm['operations'], expected_operations)

        ## Surge Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-Surge-C-100')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing Surge alarm state"):
            
            self.assertIsNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Normal')
            self.assertEqual(alarm['name'], 'Alarm-Surge-C-100')
            self.assertEqual(alarm['tag'], 'C-100')
            self.assertEqual(alarm['mnemonic'], 'NORM')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Normal')
            self.assertEqual(alarm['triggered'], False)
            self.assertEqual(alarm['acknowledged'], True)
            self.assertEqual(alarm['value'], surge_value)
            self.assertEqual(alarm['type'], 'BOOL')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'not active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'active', 
                'suppress by design': 'active', 
                'unsuppressed': 'not active', 
                'out of service': 'active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertDictEqual(alarm['operations'], expected_operations)

        ## Low Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-L')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing Low alarm state"):
            
            self.assertIsNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Normal')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-L')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'NORM')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Normal')
            self.assertEqual(alarm['triggered'], False)
            self.assertEqual(alarm['acknowledged'], True)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'LOW')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'not active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'active', 
                'suppress by design': 'active', 
                'unsuppressed': 'not active', 
                'out of service': 'active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertDictEqual(alarm['operations'], expected_operations)

        ## Low Low Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-LL')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertIsNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Normal')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-LL')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'NORM')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Normal')
            self.assertEqual(alarm['triggered'], False)
            self.assertEqual(alarm['acknowledged'], True)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'LOW-LOW')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'not active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'active', 
                'suppress by design': 'active', 
                'unsuppressed': 'not active', 
                'out of service': 'active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertDictEqual(alarm['operations'], expected_operations)

        # Iteration 2
        value = 102.0
        tag_engine.write_tag('PT-100', value)
        for tag, *args in self.__tags:

            alarm_manager.execute(tag)

        ## HIGH Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-H')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing HIGH alarm state"):
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Unacknowledged')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-H')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'UNACK')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Abnormal')
            self.assertEqual(alarm['triggered'], True)
            self.assertEqual(alarm['acknowledged'], False)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'HIGH')
            self.assertEqual(alarm['audible'], True)
            expected_operations = {
                'acknowledge': 'active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)

        # Iteration 3
        value = 112
        tag_engine.write_tag('PT-100', value)
        for tag, *args in self.__tags:

            alarm_manager.execute(tag)
        
        ## HIGH - HIGH Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-HH')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing HIGH-HIGH alarm state"):
            
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Unacknowledged')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-HH')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'UNACK')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Abnormal')
            self.assertEqual(alarm['triggered'], True)
            self.assertEqual(alarm['acknowledged'], False)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'HIGH-HIGH')
            self.assertEqual(alarm['audible'], True)
            expected_operations = {
                'acknowledge': 'active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)

        # ACKNOWLEDGE HIGH-HIGH ALARM
        ## HIGH Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-HH')
        alarm = alarm_manager.get_alarm(_alarm.id)
        alarm.acknowledge()
        alarm = alarm.serialize()
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNotNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Acknowledged')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-HH')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'ACKED')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Abnormal')
            self.assertEqual(alarm['triggered'], True)
            self.assertEqual(alarm['acknowledged'], True)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'HIGH-HIGH')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'not active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)


        # Iteration 4
        value = 45.0
        surge_value = True
        tag_engine.write_tag('PT-100', value)
        tag_engine.write_tag('C-100', surge_value)
        for tag, *args in self.__tags:

            alarm_manager.execute(tag)
        
        ## HIGH Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-H')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing HIGH alarm state"):
            
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'RTN Unacknowledged')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-H')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'RTNUN')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Normal')
            self.assertEqual(alarm['triggered'], False)
            self.assertEqual(alarm['acknowledged'], False)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'HIGH')
            self.assertEqual(alarm['audible'], False)
            expected_operations = {
                'acknowledge': 'active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)

        ## Surge Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-Surge-C-100')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing Surge alarm state"):
            
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Unacknowledged')
            self.assertEqual(alarm['name'], 'Alarm-Surge-C-100')
            self.assertEqual(alarm['tag'], 'C-100')
            self.assertEqual(alarm['mnemonic'], 'UNACK')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Abnormal')
            self.assertEqual(alarm['triggered'], True)
            self.assertEqual(alarm['acknowledged'], False)
            self.assertEqual(alarm['value'], surge_value)
            self.assertEqual(alarm['type'], 'BOOL')
            self.assertEqual(alarm['audible'], True)
            expected_operations = {
                'acknowledge': 'active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)

        ## Low Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-L')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing Low alarm state"):
            
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Unacknowledged')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-L')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'UNACK')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Abnormal')
            self.assertEqual(alarm['triggered'], True)
            self.assertEqual(alarm['acknowledged'], False)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'LOW')
            self.assertEqual(alarm['audible'], True)
            expected_operations = {
                'acknowledge': 'active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)

        # Iteration 5
        value = 15.0
        tag_engine.write_tag('PT-100', value)
        for tag, *args in self.__tags:

            alarm_manager.execute(tag)

        ## Low Low Alarm
        _alarm = AlarmsDB.read_by_name('Alarm-PT-100-LL')
        alarm = alarm_manager.get_alarm(_alarm.id).serialize()
        with self.subTest("Testing Low-Low alarm state"):
            
            self.assertIsNotNone(alarm['timestamp'])
            self.assertIsNone(alarm['acknowledged_timestamp'])
            self.assertEqual(alarm['state'], 'Unacknowledged')
            self.assertEqual(alarm['name'], 'Alarm-PT-100-LL')
            self.assertEqual(alarm['tag'], 'PT-100')
            self.assertEqual(alarm['mnemonic'], 'UNACK')
            self.assertEqual(alarm['enabled'], True)
            self.assertEqual(alarm['process'], 'Abnormal')
            self.assertEqual(alarm['triggered'], True)
            self.assertEqual(alarm['acknowledged'], False)
            self.assertEqual(alarm['value'], value)
            self.assertEqual(alarm['type'], 'LOW-LOW')
            self.assertEqual(alarm['audible'], True)
            expected_operations = {
                'acknowledge': 'active', 
                'enable': 'not active', 
                'disable': 'active', 
                'silence': 'not active', 
                'shelve': 'not active', 
                'suppress by design': 'not active', 
                'unsuppressed': 'not active', 
                'out of service': 'not active', 
                'return to service': 'not active', 
                'reset': 'active'
            }
            self.assertEqual(alarm['operations'], expected_operations)