import unittest
from pyhades.tags import UnitConversion


class TestUnitConversion(unittest.TestCase):

    def setUp(self) -> None:

        return super().setUp()

    def tearDown(self) -> None:

        return super().tearDown()

    def testLengthUnitConversion(self):

        # Test 0
        value = 10
        unit = 'meters'
        to = 'meters'

        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 10, 5)
        
        # Test 1
        value = 10
        unit = 'meters'
        to = 'inches'

        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 393.7008, 5)

        # Test 2
        unit = 'feet'
        to = 'inches'

        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 120, 5)

        # Test 3
        unit = 'feet'
        to = 'meters'

        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 3.048, 5)

    def testAreaUnitConversion(self):

        value = 10
        unit = 'meter_squared'
        to = 'inch_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 15500.03, 5)

        value = 1
        unit = 'inch_squared'
        to = 'meter_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.000645, 5)

        value = 1
        unit = 'yard_squared'
        to = 'foot_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 9, 5)

        value = 100
        unit = 'centimeter_squared'
        to = 'meter_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.01, 5)

    def testVolumeUnitConversion(self):

        value = 1
        unit = 'meter_cube'
        to = 'liter'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1000, 3)

        value = 1
        unit = 'us_gallons'
        to = 'inch_cube'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 231, 3)

        value = 1
        unit = 'imperial_gallons'
        to = 'us_barrel_oil'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.028593, 5)

    def testMassUnitConversion(self):

        value = 1
        unit = 'grams'
        to = 'pounds'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.002205, 5)

        value = 1
        unit = 'grams'
        to = 'grams'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.0, 5)

        value = 1
        unit = 'ounces'
        to = 'grams'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 28.3495, 3)

        value = 1
        unit = 'pounds'
        to = 'ounces'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 16, 3)

        value = 10 ** -9
        unit = 'gigagrams'
        to = 'grams'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.0, 3)

        value = 10 ** 9
        unit = 'nanograms'
        to = 'grams'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.0, 3)

    def testDensityUnitConversion(self):

        value = 1
        unit = 'gram_mililiter'
        to = 'pound_foot_cube'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 62.422, 3)

        value = 1
        unit = 'pound_inch_cube'
        to = 'gram_mililiter'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 27.68, 3)

        value = 1
        unit = 'kilogram_meter_cube'
        to = 'pound_foot_cube'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.062422, 5)

    def testVolumetricLiquidFlowUnitConversion(self):

        value = 1
        unit = 'liter_second'
        to = 'meter_cube_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 3.6, 3)

        value = 1
        unit = 'foot_cube_hour'
        to = 'us_barrels_oil_day'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 4.275, 3)

        value = 1
        unit = 'us_gallons_minute'
        to = 'liter_second'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.06309, 5)

    def testVolumetricGasFlowUnitConversion(self):

        value = 1
        unit = 'normal_meter_cube_hour'
        to = 'standard_cubic_feet_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 35.31073, 5)

        value = 1
        unit = 'standard_cubic_feet_minute'
        to = 'normal_meter_cube_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.699, 3)

        value = 1
        unit = 'standard_cubic_feet_minute'
        to = 'standard_cubic_feet_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 59.99294, 3)

    def testMassFlowUnitConversion(self):

        value = 1
        unit = 'kilogram_hour'
        to = 'ton_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.001, 5)

        value = 1
        unit = 'kilogram_second'
        to = 'kilogram_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 3600, 3)

        value = 1
        unit = 'pound_hour'
        to = 'ton_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.000454, 3)

    def testMolarFlowUnitConversion(self):

        value = 1
        unit = 'kilomole_hour'
        to = 'kilomole_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.0, 5)

        value = 1
        unit = 'kilomole_second'
        to = 'kilomole_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 3600, 3)

        value = 1
        unit = 'kilomole_minute'
        to = 'kilomole_second'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1 / 60, 3)

    def testPressuresUnitConversion(self):

        value = 1
        unit = 'megapascal'
        to = 'pound_squared_inch'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 145.03, 5)

        value = 1
        unit = 'megapascal'
        to = 'atmospheres'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 9.8717, 3)

        value = 1
        unit = 'milimeter_of_mercury'
        to = 'kilopascal'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.133333, 3)

        value = 1
        unit = 'inches_of_mercury'
        to = 'meters_of_water'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.345299, 5)

        value = 1
        unit = 'bar'
        to = 'pascal'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 100000, 3)

        value = 1
        unit = 'foot_of_water'
        to = 'inches_of_water'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 11.9992, 5)

    def testSpeedUnitConversion(self):

        value = 1
        unit = 'foot_minute'
        to = 'meter_second'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.005079999, 5)

        value = 100
        unit = 'miles_hour'
        to = 'kilometer_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 160.934, 3)

    def testDynamicViscosityUnitConversion(self):

        value = 1
        unit = 'poise'
        to = 'centipoise'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 100, 5)

        value = 1
        unit = 'poise'
        to = 'pound_foot_second'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.067197, 5)

    def testKinematicViscosityUnitConversion(self):

        value = 1
        unit = 'foot_squared_second'
        to = 'centistoke'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 92903, 3)

        value = 1
        unit = 'meter_squared_second'
        to = 'stoke'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 10000, 3)

    def testTemperatureUnitConversion(self):

        value = 50
        unit = 'degree_celsius'
        to = 'degree_fahrenheit'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 122, 3)

        value = 50
        unit = 'degree_fahrenheit'
        to = 'degree_celsius'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 10, 3)

        value = 273.15
        unit = 'kelvin'
        to = 'degree_celsius'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.0, 3)

        value = 300
        unit = 'kelvin'
        to = 'degree_fahrenheit'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 80.33, 3)

        value = 300
        unit = 'kelvin'
        to = 'rankine'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 540, 3)

        value = 540
        unit = 'rankine'
        to = 'degree_fahrenheit'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 80.33, 3)

        value = 540
        unit = 'rankine'
        to = 'degree_celsius'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 26.85, 3)

        value = 25
        unit = 'degree_celsius'
        to = 'degree_celsius'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 25.0, 3)

    def testTimeUnitConversion(self):

        value = 1
        unit = 'day'
        to = 'minute'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1440, 3)

        value = 60
        unit = 'minute'
        to = 'hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1, 3)

        value = 86400
        unit = 'second'
        to = 'day'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1, 3)

    def testConductivityUnitConversion(self):

        value = 1
        unit = 'british_thermal_unit_inch_hour_foot_squared_degree_fahrenheit'
        to = 'watt_meter_kelvin'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.14413, 3)

        value = 1
        unit = 'watt_meter_kelvin'
        to = 'british_thermal_unit_inch_hour_foot_squared_degree_fahrenheit'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 6.938, 3)

    def testEnergyUnitConversion(self):

        value = 1000000
        unit = 'joule'
        to = 'kilowatt_hour'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.277778, 3)

        value = 1
        unit = 'british_thermal_unit'
        to = 'joule'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1055.06, 3)

        value = 1
        unit = 'calories'
        to = 'feet_pound_force'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 3.08596, 3)

    def testPowerUnitConversion(self):

        value = 1
        unit = 'watt'
        to = 'horse_power'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.00134102, 3)

        value = 1
        unit = 'british_thermal_unit_second'
        to = 'calories_second'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 252.1654, 3)

        value = 1
        unit = 'feet_pound_force_second'
        to = 'watt'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.3557, 3)

    def testAccelerationUnitConversion(self):

        value = 1
        unit = 'meter_second_squared'
        to = 'mile_second_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 0.0006214, 3)

        value = 1
        unit = 'mile_second_squared'
        to = 'meter_second_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1609.344, 3)

        value = 1
        unit = 'meter_second_squared'
        to = 'meter_second_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 1.00, 3)

        value = 1
        unit = 'feet_second_squared'
        to = 'inch_second_squared'
        new_value = UnitConversion.convert(value, from_unit=unit, to_unit=to)
        self.assertAlmostEqual(new_value, 12, 3)
