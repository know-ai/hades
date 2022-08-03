import unittest
import json
from enum import Enum
from pyhades.alarms import AlarmState, States, Status

# States Values
NORMAL = "Normal"
UNACKNOWLEDGED = "Unacknowledged"
ACKNOWLEDGED = "Acknowledged"
RTN_UNACKNOWLEDGED = "RTN Unacknowledged"
SHELVED = "Shelved"
SUPPRESS_BY_DESIGN = "Suppressed By Design"
OUT_OF_SERVICE = "Out Of Service"

# States Names
NORM = "NORM"
UNACK = "UNACK"
ACKED = "ACKED"
RTNUN = "RTNUN"
SHLVD = "SHLVD"
DSUPR = "DSUPR"
OOSRV = "OOSRV"

# Status Values
ACTIVE = "Active"
NOT_ACTIVE = "Not Active"
ANNUNCIATED = "Annunciated"
NOT_ANNUNCIATED = "Not Annunciated"
NOT_ACTIVE_OR_ACTIVE = "Not Active or Active"
SUPPRESSED = "Suppressed"
NOT_APPLICABLE = "Not Applicable"
ABNORMAL = "Abnormal"

# Status Names
ACTV = "ACTV"
NACTV = "NACTV"
ANNCTD = "ANNCTD"
NANNCTD = "NANNCTD"
OR = "OR"
SUPR = "SUPR"
NA = "NA"
ABNORM = "ABNORM"

class TestAlarmState(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def testStatesClassType(self):

        self.assertIsInstance(States('Normal'), Enum)

    def testStatusClassType(self):

        self.assertIsInstance(Status('Normal'), Enum)

    def testStatesNames(self):

        with self.subTest("Testing NORM State name"):
            
            state = States(NORMAL)
            self.assertEqual(state.name, NORM)

        with self.subTest("Testing UNACK State name"):
            
            state = States(UNACKNOWLEDGED)
            self.assertEqual(state.name, UNACK)
        
        with self.subTest("Testing ACKED State name"):
            
            state = States(ACKNOWLEDGED)
            self.assertEqual(state.name, ACKED)

        with self.subTest("Testing RTNUN State name"):
            
            state = States(RTN_UNACKNOWLEDGED)
            self.assertEqual(state.name, RTNUN)

        with self.subTest("Testing SHLVD State name"):
            
            state = States(SHELVED)
            self.assertEqual(state.name, SHLVD)

        with self.subTest("Testing DSUPR State name"):
            
            state = States(SUPPRESS_BY_DESIGN)
            self.assertEqual(state.name, DSUPR)

        with self.subTest("Testing OOSRV State name"):
            
            state = States(OUT_OF_SERVICE)
            self.assertEqual(state.name, OOSRV)

    def testStatesValues(self):

        with self.subTest("Testing NORM State value"):
            
            state = States(NORMAL)
            self.assertEqual(state.value, NORMAL)

        with self.subTest("Testing UNACK State value"):
            
            state = States(UNACKNOWLEDGED)
            self.assertEqual(state.value, UNACKNOWLEDGED)
        
        with self.subTest("Testing ACKED State value"):
            
            state = States(ACKNOWLEDGED)
            self.assertEqual(state.value, ACKNOWLEDGED)

        with self.subTest("Testing RTNUN State value"):
            
            state = States(RTN_UNACKNOWLEDGED)
            self.assertEqual(state.value, RTN_UNACKNOWLEDGED)

        with self.subTest("Testing SHLVD State value"):
            
            state = States(SHELVED)
            self.assertEqual(state.value, SHELVED)

        with self.subTest("Testing DSUPR State value"):
            
            state = States(SUPPRESS_BY_DESIGN)
            self.assertEqual(state.value, SUPPRESS_BY_DESIGN)

        with self.subTest("Testing OOSRV State value"):
            
            state = States(OUT_OF_SERVICE)
            self.assertEqual(state.value, OUT_OF_SERVICE)

    def testStatusNames(self):

        with self.subTest("Testing ACTV Status name"):
            
            state = Status(ACTIVE)
            self.assertEqual(state.name, ACTV)

        with self.subTest("Testing NACTV Status name"):
            
            state = Status(NOT_ACTIVE)
            self.assertEqual(state.name, NACTV)
        
        with self.subTest("Testing ANNCTD Status name"):
            
            state = Status(NOT_ANNUNCIATED)
            self.assertEqual(state.name, NANNCTD)

        with self.subTest("Testing OR Status name"):
            
            state = Status(NOT_ACTIVE_OR_ACTIVE)
            self.assertEqual(state.name, OR)

        with self.subTest("Testing SUPR Status name"):
            
            state = Status(SUPPRESSED)
            self.assertEqual(state.name, SUPR)

        with self.subTest("Testing NA State name"):
            
            state = Status(NOT_APPLICABLE)
            self.assertEqual(state.name, NA)

        with self.subTest("Testing NORM Status name"):
            
            state = Status(NORMAL)
            self.assertEqual(state.name, NORM)

        with self.subTest("Testing ABNORM Status name"):
            
            state = Status(ABNORMAL)
            self.assertEqual(state.name, ABNORM)

    def testStatusValues(self):

        with self.subTest("Testing ACTV Status value"):
            
            state = Status(ACTIVE)
            self.assertEqual(state.value, ACTIVE)

        with self.subTest("Testing NACTV Status value"):
            
            state = Status(NOT_ACTIVE)
            self.assertEqual(state.value, NOT_ACTIVE)
        
        with self.subTest("Testing ANNCTD Status value"):
            
            state = Status(NOT_ANNUNCIATED)
            self.assertEqual(state.value, NOT_ANNUNCIATED)

        with self.subTest("Testing OR Status value"):
            
            state = Status(NOT_ACTIVE_OR_ACTIVE)
            self.assertEqual(state.value, NOT_ACTIVE_OR_ACTIVE)

        with self.subTest("Testing SUPR Status value"):
            
            state = Status(SUPPRESSED)
            self.assertEqual(state.value, SUPPRESSED)

        with self.subTest("Testing NA State value"):
            
            state = Status(NOT_APPLICABLE)
            self.assertEqual(state.value, NOT_APPLICABLE)

        with self.subTest("Testing NORM Status value"):
            
            state = Status(NORMAL)
            self.assertEqual(state.value, NORMAL)

        with self.subTest("Testing ABNORM Status value"):
            
            state = Status(ABNORMAL)
            self.assertEqual(state.value, ABNORMAL)

    def testAlarmStateValues(self):
        
        states = [alarm_state.state for alarm_state in AlarmState._states]
        valid_states = [
            States.NORM.value,
            States.UNACK.value,
            States.ACKED.value,
            States.RTNUN.value,
            States.SHLVD.value,
            States.DSUPR.value,
            States.OOSRV.value
        ]
        self.assertListEqual(states, valid_states)

    def testAlarmStateMnemonic(self):

        mnemonics = [alarm_state.mnemonic for alarm_state in AlarmState._states]
        valid_mnemonics = [
            States.NORM.name,
            States.UNACK.name,
            States.ACKED.name,
            States.RTNUN.name,
            States.SHLVD.name,
            States.DSUPR.name,
            States.OOSRV.name
        ]
        self.assertListEqual(mnemonics, valid_mnemonics)

    def testNORMStateAttrs(self):

        with self.subTest("Testing process_condition NORM State attribute"):

            self.assertEqual(AlarmState.NORM.process_condition, Status.NORM.value)

        with self.subTest("Testing is_triggered NORM State attribute"):

            self.assertEqual(AlarmState.NORM.is_triggered, False)
        
        with self.subTest("Testing alarm_status NORM State attribute"):

            self.assertEqual(AlarmState.NORM.alarm_status, Status.NACTV.value)
        
        with self.subTest("Testing annunciate_status NORM State attribute"):

            self.assertEqual(AlarmState.NORM.annunciate_status, Status.NANNCTD.value)

        with self.subTest("Testing acknowledge_status NORM State attribute"):

            self.assertEqual(AlarmState.NORM.acknowledge_status, States.ACKED.value)

        with self.subTest("Testing audible NORM State attribute"):

            self.assertEqual(AlarmState.NORM.audible, False)

        with self.subTest("Testing color NORM State attribute"):

            self.assertEqual(AlarmState.NORM.color, False)

        with self.subTest("Testing symbol NORM State attribute"):

            self.assertEqual(AlarmState.NORM.symbol, False)

        with self.subTest("Testing blinking NORM State attribute"):

            self.assertEqual(AlarmState.NORM.blinking, False)

    def testUNACKStateAttrs(self):

        with self.subTest("Testing process_condition UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.process_condition, Status.ABNORM.value)

        with self.subTest("Testing is_triggered UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.is_triggered, True)
        
        with self.subTest("Testing alarm_status UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.alarm_status, Status.ACTV.value)
        
        with self.subTest("Testing annunciate_status UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.annunciate_status, Status.ANNCTD.value)

        with self.subTest("Testing acknowledge_status UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.acknowledge_status, States.UNACK.value)

        with self.subTest("Testing audible UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.audible, True)

        with self.subTest("Testing color UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.color, True)

        with self.subTest("Testing symbol UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.symbol, True)

        with self.subTest("Testing blinking UNACK State attribute"):

            self.assertEqual(AlarmState.UNACK.blinking, True)

    def testACKEDStateAttrs(self):

        with self.subTest("Testing process_condition ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.process_condition, Status.ABNORM.value)

        with self.subTest("Testing is_triggered ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.is_triggered, True)
        
        with self.subTest("Testing alarm_status ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.alarm_status, Status.ACTV.value)
        
        with self.subTest("Testing annunciate_status ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.annunciate_status, Status.ANNCTD.value)

        with self.subTest("Testing acknowledge_status ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.acknowledge_status, States.ACKED.value)

        with self.subTest("Testing audible ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.audible, False)

        with self.subTest("Testing color ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.color, True)

        with self.subTest("Testing symbol ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.symbol, True)

        with self.subTest("Testing blinking ACKED State attribute"):

            self.assertEqual(AlarmState.ACKED.blinking, False)
    
    def testRTNUNStateAttrs(self):

        with self.subTest("Testing process_condition RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.process_condition, Status.NORM.value)

        with self.subTest("Testing is_triggered RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.is_triggered, False)
        
        with self.subTest("Testing alarm_status RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.alarm_status, Status.NACTV.value)
        
        with self.subTest("Testing annunciate_status RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.annunciate_status, Status.ANNCTD.value)

        with self.subTest("Testing acknowledge_status RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.acknowledge_status, States.UNACK.value)

        with self.subTest("Testing audible RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.audible, False)

        with self.subTest("Testing color RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.color, True)

        with self.subTest("Testing symbol RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.symbol, True)

        with self.subTest("Testing blinking RTNUN State attribute"):

            self.assertEqual(AlarmState.RTNUN.blinking, False)

    def testSHLVDStateAttrs(self):

        with self.subTest("Testing process_condition SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.process_condition, Status.NORM.value)

        with self.subTest("Testing is_triggered SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.is_triggered, False)
        
        with self.subTest("Testing alarm_status SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.alarm_status, Status.OR.value)
        
        with self.subTest("Testing annunciate_status SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.annunciate_status, Status.SUPR.value)

        with self.subTest("Testing acknowledge_status SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.acknowledge_status, Status.NA.value)

        with self.subTest("Testing audible SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.audible, False)

        with self.subTest("Testing color SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.color, False)

        with self.subTest("Testing symbol SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.symbol, True)

        with self.subTest("Testing blinking SHLVD State attribute"):

            self.assertEqual(AlarmState.SHLVD.blinking, False)

    def testDSUPRStateAttrs(self):

        with self.subTest("Testing process_condition DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.process_condition, Status.NORM.value)

        with self.subTest("Testing is_triggered DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.is_triggered, False)
        
        with self.subTest("Testing alarm_status DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.alarm_status, Status.OR.value)
        
        with self.subTest("Testing annunciate_status DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.annunciate_status, Status.SUPR.value)

        with self.subTest("Testing acknowledge_status DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.acknowledge_status, Status.NA.value)

        with self.subTest("Testing audible DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.audible, False)

        with self.subTest("Testing color DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.color, False)

        with self.subTest("Testing symbol DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.symbol, True)

        with self.subTest("Testing blinking DSUPR State attribute"):

            self.assertEqual(AlarmState.DSUPR.blinking, False)

    def testOOSRVStateAttrs(self):

        with self.subTest("Testing process_condition OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.process_condition, Status.NORM.value)

        with self.subTest("Testing is_triggered OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.is_triggered, False)
        
        with self.subTest("Testing alarm_status OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.alarm_status, Status.OR.value)
        
        with self.subTest("Testing annunciate_status OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.annunciate_status, Status.SUPR.value)

        with self.subTest("Testing acknowledge_status OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.acknowledge_status, Status.NA.value)

        with self.subTest("Testing audible OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.audible, False)

        with self.subTest("Testing color OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.color, False)

        with self.subTest("Testing symbol OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.symbol, True)

        with self.subTest("Testing blinking OOSRV State attribute"):

            self.assertEqual(AlarmState.OOSRV.blinking, False)

    def testGetAlarmStateByName(self):

        alarm_states = [alarm_state.state for alarm_state in AlarmState._states]
        valid_alarm_states = [
            States.NORM.value,
            States.UNACK.value,
            States.ACKED.value,
            States.RTNUN.value,
            States.SHLVD.value,
            States.DSUPR.value,
            States.OOSRV.value
        ]
        self.assertListEqual( alarm_states, valid_alarm_states)

    def testAlarmStatesAreJsonable(self):
        
        are_jsonable = all([self.is_jsonable(alarm_state) for alarm_state in AlarmState._states])

        self.assertTrue(are_jsonable)
            
    def is_jsonable(self, alarm_state):
        try:
            json.dumps(alarm_state.serialize())
            return True
        except:
            return False
