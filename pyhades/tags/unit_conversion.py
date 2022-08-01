class UnitConversion:
    r"""
    Documentation
    """
    # Length Unit
    meters = {
        'centimeters': 100,
        'milimeters': 1000,
        'kilometers': 0.001, 
        'inches': 39.37008,
        'feet': 3.28084,
        'yards': 1.093613,
        'miles': 0.000621
    }
    # Area Unit
    meter_square = {
        'inch_square': 1550.003,
        'foot_square': 10.76391,
        'yard_square': 1.19599,
        'mile_square': 0.0000003861
    }
    # Volume Unit
    meter_cube = {
        'liter': 1000,
        'mililiter': 10 ** 6,
        'inch_cube': 61023.7,
        'foot_cube': 35.3147,
        'us_gallons': 264.172,
        'imperial_gallons': 219.969,
        'us_barrel_oil': 6.28981
    }
    # Mass Unit
    grams = {
        'kilograms': 10 ** -3,
        'metric_tonnes': 0.000001,
        'pounds': 0.00220462,
        'ounces': 0.035274
    }
    # Density Unit
    gram_mililiter = {
        'kilogram_meter_cube': 1000,
        'pound_foot_cube': 62.42197,
        'pound_inch_cube': 0.036127
    }
    # Volumetric Liquid Flow
    liter_second = {
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
        'pound_hour': 2.204586,
        'kilogram_second': 0.0002777778,
        'ton_hour': 0.001
    }
    # Pressure
    megapascal = {
        'pascal': 1000000,
        'inches_of_water': 0.0040144523761 * 1000000,
        'inches_of_mercury': 0.000295333775 * 1000000,
        'centimeter_of_mercury': 0.000750187 * 1000000,
        'foot_of_water': 0.00033456 * 1000000,
        'meters_of_water': 0.00010197838 * 1000000,
        'kilopascal': 1000,
        'pound_square_inch': 145.03,
        'bar': 10,
        'kilogram_force_centimeter_square': 10.197,
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
        'foot_square_second': 0.001076391505118,
        'meter_square_second': 0.0001
    }
    # Time
    day = {
        'hour': 24,
        'minute': 24 * 60,
        'second': 24 * 60 * 60,
        'milisecond': 24 * 60 * 60 * 1000,
        'microsecond': 24 * 60 * 60 * 1000 * 1000
    }
    # Conductivity

    # Energy
    joule = {
        'newton_meter': 1,
        'ergios': 10 ** -7,

    }

    # Acceleration

    # Radiation


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

                if _from.startswith('degree'):

                    return UnitConversion.__temperature_converter(value, _from, _to)
                
                if _from==key:

                    if _to in _value.keys():

                        multiplier = _value[f'{_to}']

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

    @staticmethod
    def __temperature_converter(value:float, _from:str, _to:str):
        r"""
        Documentation here
        """
        if _from=='degree_celsius':

            if _to=='degree_fahrenheit':

                return (value * 9 / 5) + 32.0

            if _to=='degree_kelvin':

                return value + 273.15

            if _to=='degree_rankine':

                return ((value * 9 / 5) + 32.0) + 459.67

        if _from=='degree_fahrenheit':

            if _to=='degree_celsius':

                return (value - 32) * (5 / 9)

            if _to=='degree_kelvin':

                return (value - 32) * (5 / 9) + 273.15

            if _to=='degree_rankine':

                return value + 459.67

        if _from=='degree_rankine':

            if _to=='degree_fahrenheit':

                return value - 459.67

            if _to=='degree_celsius':

                return ((value - 459.67) - 32) * (5 / 9)

            if _to=='degree_kelvin':

                return ((value - 459.67) - 32) * (5 / 9) + 273.15

        if _from=='degree_kelvin':

            if _to=='degree_fahrenheit':

                return ((value - 273.15) * 9 / 5) + 32.0

            if _to=='degree_celsius':

                return value - 273.15

            if _to=='degree_rankine':

                return ((value - 273.15) * 9 / 5) + 32.0 + 459.67