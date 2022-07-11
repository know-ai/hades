import os
import unittest
from pyhades import PyHades
from pyhades.dbmodels import AlarmsDB
from pyhades.tags import CVTEngine



class TestDBModelsFromConfigFile(unittest.TestCase):
    r"""
    Documentation here
    """
    engine = CVTEngine()

    def setUp(self) -> None:

        # Init DB
        self.dbfile = "app.db"
        self.app = PyHades()
        self.app.set_mode('Development')
        config_file = os.path.join('pyhades', 'tests', 'config.yml')
        self.app.set_db_from_config_file(config_file)
        self.engine.set_config(config_file)     
        self.app.define_alarm_from_config_file(config_file)

        return super().setUp()

    def tearDown(self) -> None:

        # # Drop DB
        # self.app.stop_db(self.db_worker)
        # self.app.drop_db(dbfile=self.dbfile)
        # del self.app
        return super().tearDown()

    def testDefineAlarm(self):
        r"""
        Documentation here
        """
        alarm_name, tag, desc, alarm_type, alarm_trigger = (
            "alarm_PT_01", 
            "PT-01", 
            "alarm for Inlet Pressure",
            "HIGH-HIGH",
            55.5
        )

        _alarm = AlarmsDB.read_by_name(name=alarm_name)

        expected_result = {
            'id': 1, 
            'name': alarm_name, 
            'tag': tag, 
            'desc': desc, 
            'alarm_type': alarm_type, 
            'trigger': alarm_trigger
        }

        self.assertEqual(_alarm.serialize(), expected_result)


if __name__=='__main__':

    unittest.main()