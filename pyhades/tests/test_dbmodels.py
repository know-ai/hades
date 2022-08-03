import unittest
from pyhades import PyHades
from pyhades.dbmodels import Units, Variables, DataTypes, Tags, AlarmsDB
from pyhades.dbmodels import AlarmTypes, AlarmPriorities, AlarmStates
from pyhades.alarms import Alarm
from datetime import datetime


class TestDBModels(unittest.TestCase):
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

        self.__tags = [
            ('PT-01', 'Pa', 'float', 'Inlet Pressure'),
            ('PT-02', 'Pa', 'float', 'Outlet Pressure'),
            ('FT-01', 'kg/s', 'float', 'Inlet Mass Flow'),
            ('FT-02', 'kg/s', 'float', 'Outlet Mass Flow')
        ]

        return super().setUp()

    def tearDown(self) -> None:

        # Drop DB
        self.app.stop_db(self.db_worker)
        self.app.drop_db(dbfile=self.dbfile)
        del self.app
        return super().tearDown()

    def testCountVariablesAdded(self):

        result = Variables.read_all()

        self.assertEqual(len(result['data']), 19)

    def testCountUnitsAdded(self):

        result = Units.read_all()

        self.assertEqual(len(result['data']), 140)

    def testCountDataTypesAdded(self):

        result = DataTypes.read_all()

        self.assertEqual(len(result['data']), 4)

    def testCountAlarmPrioritiesAdded(self):

        result = AlarmPriorities.read_all()

        self.assertEqual(len(result['data']), 6)

    def testCountAlarmTypesAdded(self):

        result = AlarmTypes.read_all()

        self.assertEqual(len(result['data']), 6)

    def testCountAlarmStatesAdded(self):

        result = AlarmStates.read_all()

        self.assertEqual(len(result['data']), 7)

    def testCountTagsAdded(self):

        for name, unit, data_type, description in self.__tags:

            Tags.create(
                name=name, 
                unit=unit, 
                data_type=data_type,
                description=description)

        result = Tags.read_all()

        self.assertEqual(len(result['data']), len(self.__tags))

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

        expected_result = {
            'id': 1, 
            'name': alarm_name, 
            'tag': tag, 
            'description': description, 
            'alarm_type': alarm_type, 
            'trigger': alarm_trigger
        }

        self.assertEqual(_alarm.serialize(), expected_result)

    def testFromConfigFile(self):
        r"""
        Documentation here
        """


if __name__=='__main__':

    unittest.main()