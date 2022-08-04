from ..dbmodels import Units


class TemperatureConverter:
    r"""
    Documentation here
    """

    def __init__(self):

        self.__valid_units = ['degree_celsius', 'degree_fahrenheit', 'kelvin', 'rankine']
        self.__value = 0

    def convert(self, value:float, from_unit:str, to_unit:str):
        r"""
        Documentation here
        """
        if isinstance(value, (float, int)):

            self.__value = value

        else:

            raise TypeError(f"{value} must be a float or int value")

        if all(elem in self.__valid_units  for elem in [from_unit.lower(), to_unit.lower()]):

            if from_unit.lower()==to_unit.lower():

                return value

            _convert = getattr(self, f"{from_unit}_to_{to_unit}")

            return _convert()

        else:

            raise KeyError(f"{from_unit} or {to_unit} are not a temperature unit valid")

    def degree_celsius_to_kelvin(self):
        r"""
        Documentation here
        """
        return self.__value + 273.15

    def degree_celsius_to_degree_fahrenheit(self):
        r"""
        Documentation here
        """
        return (self.__value * 9 / 5) + 32.0

    def degree_fahrenheit_to_rankine(self):
        r"""
        Documentation here
        """
        return self.__value + 459.67

    def degree_fahrenheit_to_degree_celsius(self):
        r"""
        Documentation here
        """
        return (self.__value - 32) * (5 / 9)

    def kelvin_to_degree_celsius(self):
        r"""
        Documentatio here
        """
        return self.__value - 273.15

    def rankine_to_degree_fahrenheit(self):
        r"""
        Documentation here
        """
        return self.__value - 459.67

    def degree_celsius_to_rankine(self):
        r"""
        Documentation here
        """
        self.__value = self.degree_celsius_to_degree_fahrenheit()
        return self.degree_fahrenheit_to_rankine()

    def rankine_to_degree_celsius(self):
        r"""
        Documentation here
        """
        self.__value = self.rankine_to_degree_fahrenheit()
        return self.degree_fahrenheit_to_degree_celsius()

    def degree_fahrenheit_to_kelvin(self):
        r"""
        Documentation here
        """
        self.__value = self.degree_fahrenheit_to_degree_celsius()
        return self.degree_celsius_to_kelvin()

    def kelvin_to_degree_fahrenheit(self):
        r"""
        Documentation here
        """
        self.__value = self.kelvin_to_degree_celsius()
        return self.degree_celsius_to_degree_fahrenheit()

    def kelvin_to_rankine(self):
        r"""
        Documentation here
        """
        self.__value = self.kelvin_to_degree_fahrenheit()
        return self.degree_fahrenheit_to_rankine()

    def rankine_to_kelvin(self):
        r"""
        Documentation here
        """
        self.__value = self.rankine_to_degree_celsius()
        return self.degree_celsius_to_kelvin()


class ConverterByMultiplier:
    r"""
    Documentation here
    """
    
    def __init__(self):
        self.__value = 0
        

    def convert(self, value:float, from_unit:str, to_unit:str):
        r"""
        Documentation here"""
        print('Hi Converter')
        self.__valid_units = [unit['name'] for unit in Units.read_all()]
        # print(f'valid units:{self.__valid_units}')


class UnitConversion:
    r"""
    Documentation
    """
    # Length Unit
    meters = {
        'exameters': 10 ** -18,
        'petameters': 10 ** -15,
        'terameters': 10 ** -12,
        'gigameters': 10 ** -9,
        'megameters': 10 ** -6,
        'kilometers': 10 ** -3, 
        'hectometers': 10 ** -2,
        'decameters': 10 ** -1,
        'decimeters': 10 ** 1,
        'centimeters': 10 ** 2,
        'milimeters': 10 ** 3,
        'micrometers': 10 ** 6,
        'nanometers': 10 ** 9,
        'picometers': 10 ** 12,
        'femtometers': 10 ** 15,
        'attometers': 10 ** 18,
        'inches': 39.37008,
        'feet': 3.28084,
        'yards': 1.093613,
        'miles': 0.000621
    }
    # Area Unit
    meter_squared = {
        'centimeter_squared': 10 ** (2 * 2),
        'milimiter_squared': 10 ** (3 * 2),
        'kilometer_squared': 10 ** (-3 * 2),
        'inch_squared': 1550.003,
        'foot_squared': 10.76391,
        'yard_squared': 1.19599,
        'mile_squared': 0.0000003861
    }
    # Volume Unit
    meter_cube = {
        'liter': 10 ** 3,
        'mililiter': 10 ** 6,
        'inch_cube': 61023.7,
        'foot_cube': 35.3147,
        'us_gallons': 264.172,
        'imperial_gallons': 219.969,
        'us_barrel_oil': 6.28981
    }
    # Mass Unit
    grams = {
        'exagrams': 10 ** -18,
        'petagrams': 10 ** -15,
        'teragrams': 10 ** -12,
        'gigagrams': 10 ** -9,
        'megagrams': 10 ** -6,
        'kilograms': 10 ** -3, 
        'hectograms': 10 ** -2,
        'decagrams': 10 ** -1,
        'decigrams': 10 ** 1,
        'centigrams': 10 ** 2,
        'miligrams': 10 ** 3,
        'micrograms': 10 ** 6,
        'nanograms': 10 ** 9,
        'picograms': 10 ** 12,
        'femtograms': 10 ** 15,
        'attograms': 10 ** 18,
        'metric_tonnes': 10 ** -6,
        'pounds': 0.00220462,
        'ounces': 0.035274
    }
    # Density Unit
    gram_mililiter = {
        'kilogram_meter_cube': 10 ** 3,
        'pound_foot_cube': 62.42197,
        'pound_inch_cube': 0.036127
    }
    # Volumetric Liquid Flow
    liter_second = { 
        "liter_hour": 3600, 
        "meter_cube_second": 10 ** -3, 
        "meter_cube_minute": (10 ** -3) * 60, 
        'foot_cube_second': 2.119093 / 60,
        'liter_minute': 60,
        'meter_cube_hour': 3.6,
        'foot_cube_minute': 2.119093,
        'foot_cube_hour': 127.1197,
        'us_gallons_minute': 15.85037,
        'us_barrels_oil_day': 543.4783
    }
    # Volumetric Gas Flow
    normal_meter_cube_hour = {
        'standard_cubic_feet_hour': 35.31073,
        'standard_cubic_feet_minute': 0.588582
    }
    # Mass Flow
    kilogram_hour = {
        "kilogram_second": 1 / (60 * 60), 
        "kilogram_minute": 1 / 60,
        "gram_second": (10 ** 3) / (60 * 60),
        "gram_minute": (10 ** 3) / 60,
        "gram_hour": 10 ** 3,
        'pound_hour': 2.204586,
        'ton_hour': 0.001
    }
    # Molar Flow
    kilomole_hour = {
        "kilomole_minute": 1 / 60, 
        "kilomole_second": 1 / 3600
    }
    # Pressure
    megapascal = {
        'pascal': 10 ** 6,
        'inches_of_water': 0.0040144523761 * 10 ** 6,
        'inches_of_mercury': 0.000295333775 * 10 ** 6,
        'centimeter_of_mercury': 0.000750187 * 10 ** 6,
        'foot_of_water': 0.00033456 * 10 ** 6,
        'meters_of_water': 0.00010197838 * 10 ** 6,
        'kilopascal': 1000,
        'pound_squared_inch': 145.03,
        'bar': 10,
        'kilogram_force_centimeter_squared': 10.197,
        'milimeter_of_mercury': 7500.2,
        'atmospheres': 9.8717
    }
    # Speed
    meter_second = {
        'meter_minute': 60,
        'kilometer_hour': 3.6,
        'foot_second': 3.28084,
        'foot_minute': 196.8504,
        'miles_hour': 2.2369356
    }
    # Dynamic Viscosity
    centipoise = {
        'poise': 0.01,
        'pound_foot_second': 0.000672
    }
    # Kinematic Viscosity
    stoke = {
        'centistoke': 100,
        'foot_squared_second': 0.001076391505118,
        'meter_squared_second': 0.0001
    }
    # Time
    day = {
        'hour': 24,
        'minute': 24 * 60,
        'second': 24 * 60 * 60,
        'milisecond': 24 * 60 * 60 * 1000,
        'microsecond': 24 * 60 * 60 * 10 ** 6
    }
    # Conductivity
    watt_meter_kelvin = {
        'british_thermal_unit_inch_hour_foot_squared_degree_fahrenheit': 6.9381117888
    }

    # Energy
    joule = {
        'newton_meter': 1,
        'ergios': 10 ** 7,
        'dynes_centimeter': 10 ** 7,
        'kilowatt_hour': 2.778 * 10 ** -7,
        'calories': 0.2390057361,
        'feet_pound_force': 0.7375621493,
        'british_thermal_unit': 9.478133944988911 * 10 ** -4
    }
    # Power
    watt = {
        'joule_second': 1.0,
        'calories_second': 0.2390057361,
        'feet_pound_force_second': 0.7375621493,
        'british_thermal_unit_second': 9.478133944988911 * 10 ** -4,
        'horse_power': 1.341 * 10 ** -3
    }
    # Acceleration
    meter_second_squared = {
        'inch_second_squared': 39.37008,
        'feet_second_squared': 3.280839895,
        'mile_second_squared': 0.00062137119
    }
    temperature_converter = TemperatureConverter()
    converter = ConverterByMultiplier()

    @classmethod
    def convert(cls, value:float, from_unit:str, to_unit:str):
        r"""
        Documentation here
        """
        _from = from_unit.lower()
        _to = to_unit.lower()
        multiplier = None
        for key, _value in cls.__dict__.items():

            if isinstance(_value, dict):

                _unit = Units.read_by_name(from_unit)
                _variable = _unit['variable'].lower()

                if _variable=='temperature':

                    return cls.temperature_converter.convert(value, _from, _to)
                
                # cls.converter.convert(value, _from, _unit)
                
                if _from==key:

                    if _to in _value.keys():

                        multiplier = _value[f'{_to}']

                        break

                    if _to==key:

                        multiplier = 1

                        break

                if _from in _value.keys():

                    if _to in _value.keys():

                        multiplier = _value[f'{_to}'] / _value[f'{_from}']

                        break

                if _from in _value.keys():

                    if _to==key:

                        multiplier = 1 / _value[f'{_from}']

                        break

        if multiplier is None:

            raise KeyError(f"Unit {_from} or {_to} is not defined")

        return value * multiplier