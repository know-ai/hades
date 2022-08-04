import os
import unittest
from pyhades.dbmodels import AlarmsDB
from pyhades.tests import app, tag_engine

class TestDBModelsFromConfigFile(unittest.TestCase):
    r"""
    Documentation here
    """

    def setUp(self) -> None:

        config_file = os.path.join('pyhades', 'tests', 'config.yml')
        app.set_db_from_config_file(config_file)
        tag_engine.set_config(config_file)     
        app.define_alarm_from_config_file(config_file)

        return super().setUp()

    def tearDown(self) -> None:

        return super().tearDown()

    def testDefineAlarm(self):
        r"""
        Documentation here
        """
        alarm_name, tag, description, alarm_type, alarm_trigger = (
            "PT_01_HH", 
            "PT-01", 
            "alarm for Inlet Pressure",
            "HIGH-HIGH",
            55.5
        )

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
