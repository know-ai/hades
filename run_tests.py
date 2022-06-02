from unittest import TestLoader, TestSuite, TextTestRunner
from pyhades.tests.test_alarm_states import TestAlarmState
from pyhades.tests.test_bool_alarms import TestBoolAlarms
from pyhades.tests.test_high_alarms import TestHighAlarms
from pyhades.tests.test_high_high_alarms import TestHighHighAlarms
from pyhades.tests.test_low_low_alarms import TestLowLowAlarms
from pyhades.tests.test_low_alarms import TestLowAlarms
from pyhades.tests.test_alarm_manager import TestAlarmManager
from pyhades.tests.test_dbmodels import TestDBModels


def suite():
    r"""
    Documentation here
    """
    tests = list()
    suite = TestSuite()
    tests.append(TestLoader().loadTestsFromTestCase(TestAlarmState))
    tests.append(TestLoader().loadTestsFromTestCase(TestBoolAlarms))
    tests.append(TestLoader().loadTestsFromTestCase(TestHighAlarms))
    tests.append(TestLoader().loadTestsFromTestCase(TestHighHighAlarms))
    tests.append(TestLoader().loadTestsFromTestCase(TestLowLowAlarms))
    tests.append(TestLoader().loadTestsFromTestCase(TestLowAlarms))
    tests.append(TestLoader().loadTestsFromTestCase(TestAlarmManager))
    tests.append(TestLoader().loadTestsFromTestCase(TestDBModels))
    suite = TestSuite(tests)
    return suite


if __name__=='__main__':
    
    runner = TextTestRunner()
    runner.run(suite())
