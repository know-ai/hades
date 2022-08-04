import unittest
from pyhades.dbmodels import Units, Variables, DataTypes, Tags, AlarmsDB
from pyhades.dbmodels import AlarmTypes, AlarmPriorities, AlarmStates
from pyhades.alarms import Alarm


class TestDBModels(unittest.TestCase):
    r"""
    Documentation here
    """

    def setUp(self) -> None:


        self.__tags = [
            ('PT-01', 'Pa', 'float', 'Inlet Pressure'),
            ('PT-02', 'Pa', 'float', 'Outlet Pressure'),
            ('FT-01', 'kg/s', 'float', 'Inlet Mass Flow'),
            ('FT-02', 'kg/s', 'float', 'Outlet Mass Flow')
        ]

        return super().setUp()

    def tearDown(self) -> None:

        return super().tearDown()

    def testCountVariablesAdded(self):

        result = Variables.read_all()

        self.assertEqual(len(result), 20)

    def testCountUnitsAdded(self):

        result = Units.read_all()

        self.assertEqual(len(result), 144)

    def testCountDataTypesAdded(self):

        result = DataTypes.read_all()

        self.assertEqual(len(result), 4)

    def testCountAlarmPrioritiesAdded(self):

        result = AlarmPriorities.read_all()

        self.assertEqual(len(result), 6)

    def testCountAlarmTypesAdded(self):

        result = AlarmTypes.read_all()

        self.assertEqual(len(result), 6)

    def testCountAlarmStatesAdded(self):

        result = AlarmStates.read_all()

        self.assertEqual(len(result), 7)

    def testDefineAlarm(self):
        r"""
        Documentation here
        """

        for name, unit, data_type, description in self.__tags:

            Tags.create(
                name=name,  
                unit=unit, 
                data_type=data_type,
                description=description)

        alarm_name, tag, description, alarm_type, alarm_trigger = (
            "alarm_PT_01", 
            "PT-01", 
            "Ejemplo High-High",
            "HIGH-HIGH",
            55.5
        )

        alarm = Alarm(name=alarm_name, tag=tag, description=description)
        alarm.set_trigger(value=alarm_trigger, _type=alarm_type)
        _alarm = AlarmsDB.read_by_name(name=alarm_name)
        _alarm_result = _alarm.serialize()
        _alarm_result.pop('id')

        expected_result = {
            'name': alarm_name, 
            'tag': tag, 
            'description': description, 
            'alarm_type': alarm_type, 
            'trigger': alarm_trigger
        }

        self.assertEqual(_alarm_result, expected_result)
