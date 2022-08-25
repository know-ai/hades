from ..dbmodels import Units
import json, os
from ..src import get_directory
from ..utils import log_detailed
from .._singleton import Singleton

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


class Converter(Singleton):
    r"""
    Documentation here
    """
    temperature_converter = TemperatureConverter()

    def __init__(self):
        # Default Units
        filename = os.path.join(get_directory('src'), 'units.json')
        f = open(filename)
        units = json.load(f)
        for unit, factors in units.items():

            setattr(self, unit, factors)

    def add_conversions(self, conversions_path:str):
        r"""
        Documentation here
        """
        f = open(conversions_path)
        try:

            conversions = json.load(f)
            if conversions:

                for unit, factors in conversions.items():

                    if not hasattr(self, unit):

                        setattr(self, unit, factors)
                    
                    else:

                        _conversions = getattr(self, unit)
                        
                        for key, factor_value in factors.items():

                            if key not in _conversions.keys():

                                _conversions[key] = factor_value

        except Exception as _err:

            message = "Error in Adding Custom Conversions"
            log_detailed(_err, message)

    def convert(self, value:float, from_unit:str, to_unit:str):
        r"""
        Documentation here
        """
        _from = from_unit.lower()
        _to = to_unit.lower()
        multiplier = None
        for key, _value in self.__dict__.items():

            if isinstance(_value, dict):

                _unit = Units.read_by_name(from_unit)
                _variable = _unit['variable'].lower()

                if _variable=='temperature':

                    return self.temperature_converter.convert(value, _from, _to)
                
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


class UnitConversion:
    r"""
    Documentation
    """
    converter = Converter()

    @classmethod
    def convert(cls, value:float, from_unit:str, to_unit:str):
        r"""
        Documentation here
        """
        return cls.converter.convert(value, from_unit=from_unit, to_unit=to_unit)

    @classmethod
    def add_conversions(cls, conversions_path:str):
        r"""
        Documentation here
        """
        cls.converter.add_conversions(conversions_path=conversions_path)