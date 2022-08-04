import unittest
from pyhades.tests import tag_engine


class TestUnitConversionFromTags(unittest.TestCase):

    def setUp(self) -> None:

        return super().setUp()

    def tearDown(self) -> None:

        return super().tearDown()

    def testLengthUnitConversion(self):

        tag_name = 'test_length_tag'
        _tag = (tag_name, 'm', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 10
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='cm')
        self.assertAlmostEqual(new_value, 1000.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='m')
        self.assertAlmostEqual(new_value, 10.0, 5)
        
        new_value = tag_engine.read_tag(tag_name, unit='in')
        self.assertAlmostEqual(new_value, 393.7008, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft')
        self.assertAlmostEqual(new_value, 32.8084, 5)

        new_value = tag_engine.read_tag(tag_name, unit='yd')
        self.assertAlmostEqual(new_value, 10.936130, 5)

        new_value = tag_engine.read_tag(tag_name, unit='km')
        self.assertAlmostEqual(new_value, 0.01, 5)

        new_value = tag_engine.read_tag(tag_name, unit='mi')
        self.assertAlmostEqual(new_value, 0.00621, 5)

    def testAreaUnitConversion(self):

        tag_name = 'test_area_tag'
        _tag = (tag_name, 'm2', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 10
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='in2')
        self.assertAlmostEqual(new_value, 15500.03, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft2')
        self.assertAlmostEqual(new_value, 107.6391, 5)


    def testVolumeUnitConversion(self):

        tag_name = 'test_volume_tag'
        _tag = (tag_name, 'm3', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 10
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='lt')
        self.assertAlmostEqual(new_value, 10000.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='US brl')
        self.assertAlmostEqual(new_value, 62.8981, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft3')
        self.assertAlmostEqual(new_value, 353.147, 5)

        new_value = tag_engine.read_tag(tag_name, unit='US gal')
        self.assertAlmostEqual(new_value, 2641.72, 5)

    def testMassUnitConversion(self):

        tag_name = 'test_mass_tag'
        _tag = (tag_name, 'g', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1000
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='kg')
        self.assertAlmostEqual(new_value, 1.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='tonne')
        self.assertAlmostEqual(new_value, 10 ** -3, 5)

        new_value = tag_engine.read_tag(tag_name, unit='lb')
        self.assertAlmostEqual(new_value, 2.20462, 5)

        new_value = tag_engine.read_tag(tag_name, unit='oz')
        self.assertAlmostEqual(new_value, 35.274, 5)

    def testDensityUnitConversion(self):

        tag_name = 'test_density_tag'
        _tag = (tag_name, 'g/ml', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='kg/m3')
        self.assertAlmostEqual(new_value, 1000, 5)

        new_value = tag_engine.read_tag(tag_name, unit='lb/ft3')
        self.assertAlmostEqual(new_value, 62.42197, 5)

        new_value = tag_engine.read_tag(tag_name, unit='lb/in3')
        self.assertAlmostEqual(new_value, 0.036127, 5)

    def testVolumetricLiquidFlowUnitConversion(self):

        tag_name = 'test_vol_liq_flow_tag'
        _tag = (tag_name, 'lt/s', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1000
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='lt/h')
        self.assertAlmostEqual(new_value, 3.6 * 10 ** 6, 5)

        new_value = tag_engine.read_tag(tag_name, unit='m3/s')
        self.assertAlmostEqual(new_value, 1.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='m3/min')
        self.assertAlmostEqual(new_value, 60, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft3/min')
        self.assertAlmostEqual(new_value, 2119.093, 5)

        new_value = tag_engine.read_tag(tag_name, unit='US brl/d')
        self.assertAlmostEqual(new_value, 543478.3, 5)

    def testVolumetricGasFlowUnitConversion(self):

        tag_name = 'test_vol_gas_flow_tag'
        _tag = (tag_name, 'Nm3/h', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='Std. ft3/h')
        self.assertAlmostEqual(new_value, 35.31073, 5)

        new_value = tag_engine.read_tag(tag_name, unit='Std. ft3/min')
        self.assertAlmostEqual(new_value, 0.588582, 5)

    def testMassFlowUnitConversion(self):

        tag_name = 'test_mass_flow_tag'
        _tag = (tag_name, 'kg/h', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1000
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='kg/s')
        self.assertAlmostEqual(new_value, 1000 / (60 * 60), 5)

        new_value = tag_engine.read_tag(tag_name, unit='kg/min')
        self.assertAlmostEqual(new_value, 1000 / 60, 5)

        new_value = tag_engine.read_tag(tag_name, unit='lb/h')
        self.assertAlmostEqual(new_value, 2204.586, 5)

        new_value = tag_engine.read_tag(tag_name, unit='tonne/h')
        self.assertAlmostEqual(new_value, 1.0, 5)

    def testMolarFlowUnitConversion(self):

        tag_name = 'test_molar_flow_tag'
        _tag = (tag_name, 'kmole/h', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1000
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='kmole/min')
        self.assertAlmostEqual(new_value, 1000 / 60, 5)

        new_value = tag_engine.read_tag(tag_name, unit='kmole/s')
        self.assertAlmostEqual(new_value, 1000 / 3600, 5)

    def testPressuresUnitConversion(self):

        tag_name = 'test_pressure_tag'
        _tag = (tag_name, 'Pa', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 10 ** 6
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='MPa')
        self.assertAlmostEqual(new_value, 1.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='inH2O')
        self.assertAlmostEqual(new_value, 4014.4523761, 5)

        new_value = tag_engine.read_tag(tag_name, unit='bar')
        self.assertAlmostEqual(new_value, 10.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='mmHg')
        self.assertAlmostEqual(new_value, 7500.2, 5)

        new_value = tag_engine.read_tag(tag_name, unit='atm')
        self.assertAlmostEqual(new_value, 9.8717, 5)

    def testSpeedUnitConversion(self):

        tag_name = 'test_speed_tag'
        _tag = (tag_name, 'm/s', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='m/min')
        self.assertAlmostEqual(new_value, 60, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft/s')
        self.assertAlmostEqual(new_value, 3.28084, 5)

        new_value = tag_engine.read_tag(tag_name, unit='km/h')
        self.assertAlmostEqual(new_value, 3.6, 5)

        new_value = tag_engine.read_tag(tag_name, unit='mi/h')
        self.assertAlmostEqual(new_value, 2.2369356, 5)

    def testDynamicViscosityUnitConversion(self):

        tag_name = 'test_dyn_visc_tag'
        _tag = (tag_name, 'cp', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1000.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='poise')
        self.assertAlmostEqual(new_value, 10.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='lb/(ft.s)')
        self.assertAlmostEqual(new_value, 0.672, 5)

    def testKinematicViscosityUnitConversion(self):

        tag_name = 'test_kin_visc_tag'
        _tag = (tag_name, 'St', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 10
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='cs')
        self.assertAlmostEqual(new_value, 1000.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft2/s')
        self.assertAlmostEqual(new_value, 0.010763915, 5)

        new_value = tag_engine.read_tag(tag_name, unit='m2/s')
        self.assertAlmostEqual(new_value, 0.001, 5)

    def testTemperatureUnitConversion(self):

        tag_name = 'test_temp_tag'
        _tag = (tag_name, 'ªC', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 300
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='K')
        self.assertAlmostEqual(new_value, 573.15, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ªF')
        self.assertAlmostEqual(new_value, 572, 5)

        new_value = tag_engine.read_tag(tag_name, unit='R')
        self.assertAlmostEqual(new_value, 1031.67, 5)

    def testTimeUnitConversion(self):

        tag_name = 'test_time_tag'
        _tag = (tag_name, 'd', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='h')
        self.assertAlmostEqual(new_value, 24, 5)

        new_value = tag_engine.read_tag(tag_name, unit='s')
        self.assertAlmostEqual(new_value, 24 * 3600, 5)

        new_value = tag_engine.read_tag(tag_name, unit='min')
        self.assertAlmostEqual(new_value, 24 * 60, 5)

    def testConductivityUnitConversion(self):

        tag_name = 'test_cond_tag'
        _tag = (tag_name, 'W/(m.K)', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='BTU.in/(h.ft2.ªF)')
        self.assertAlmostEqual(new_value, 6.9381117888, 5)

    def testEnergyUnitConversion(self):

        tag_name = 'test_ener_tag'
        _tag = (tag_name, 'J', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='N.m')
        self.assertAlmostEqual(new_value, 1.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='erg')
        self.assertAlmostEqual(new_value, 10 ** 7, 5)

        new_value = tag_engine.read_tag(tag_name, unit='cal')
        self.assertAlmostEqual(new_value, 0.2390057361, 5)

        new_value = tag_engine.read_tag(tag_name, unit='kWh')
        self.assertAlmostEqual(new_value, 2.778 * 10 ** -7, 5)

        new_value = tag_engine.read_tag(tag_name, unit='BTU')
        self.assertAlmostEqual(new_value, 9.478133944988911 * 10 ** -4, 5)

    def testPowerUnitConversion(self):

        tag_name = 'test_power_tag'
        _tag = (tag_name, 'W', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='J/s')
        self.assertAlmostEqual(new_value, 1.0, 5)

        new_value = tag_engine.read_tag(tag_name, unit='cal/s')
        self.assertAlmostEqual(new_value, 0.2390057361, 5)

        new_value = tag_engine.read_tag(tag_name, unit='BTU/s')
        self.assertAlmostEqual(new_value, 9.478133944988911 * 10 ** -4, 5)

        new_value = tag_engine.read_tag(tag_name, unit='hp')
        self.assertAlmostEqual(new_value, 1.341 * 10 ** -3, 5)

    def testAccelerationUnitConversion(self):

        tag_name = 'test_acc_tag'
        _tag = (tag_name, 'm/s2', 'float', 'Test Tag Description')
        tag_engine.set_tag(*_tag)
        value = 1.0
        tag_engine.write_tag(tag_name, value)

        new_value = tag_engine.read_tag(tag_name, unit='in/s2')
        self.assertAlmostEqual(new_value, 39.37008, 5)

        new_value = tag_engine.read_tag(tag_name, unit='ft/s2')
        self.assertAlmostEqual(new_value, 3.280839895, 5)

        new_value = tag_engine.read_tag(tag_name, unit='mi/s2')
        self.assertAlmostEqual(new_value, 0.00062137119, 5)
