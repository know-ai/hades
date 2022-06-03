import unittest
from pyhades import PyHades
from pyhades.dbmodels import Units, Variables, DataTypes, Tags
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

        self.__variables = [
            'Pressure',
            'Temperature',
            'Mass_Flow'
        ]

        self.__units = [
            ('Pa', 'Pressure'),
            ('Celsius', 'Temperature'),
            ('kg/s', 'Mass_Flow')
        ]

        self.__data_types = [
            'float',
            'int',
            'str',
            'bool'
        ]

        self.__tags = [
            ('PT-01', datetime.now(), 0.5, 'Pa', 'float', 'Inlet Pressure'),
            ('PT-02', datetime.now(), 0.5, 'Pa', 'float', 'Outlet Pressure'),
            ('FT-01', datetime.now(), 0.5, 'kg/s', 'float', 'Inlet Mass Flow'),
            ('FT-02', datetime.now(), 0.5, 'kg/s', 'float', 'Outlet Mass Flow')
        ]

        return super().setUp()

    def tearDown(self) -> None:

        # Drop DB
        self.app.stop_db(self.db_worker)
        self.app.drop_db(dbfile=self.dbfile)
        del self.app
        return super().tearDown()

    def testCountVariablesAdded(self):

        for variable_name in self.__variables:

            Variables.create(name=variable_name)

        result = Variables.read_all()

        self.assertEqual(len(result['data']), len(self.__variables))

    def testCountUnitsAdded(self):

        for variable_name in self.__variables:

            Variables.create(name=variable_name)

        for name, variable in self.__units:

            Units.create(name=name, variable=variable)

        result = Units.read_all()

        self.assertEqual(len(result['data']), len(self.__units))

    def testCountDataTypesAdded(self):

        for datatype_name in self.__data_types:

            DataTypes.create(name=datatype_name)

        result = DataTypes.read_all()

        self.assertEqual(len(result['data']), len(self.__data_types))

    def testCountTagsAdded(self):
        
        for variable_name in self.__variables:

            Variables.create(name=variable_name)

        for name, variable in self.__units:

            Units.create(name=name, variable=variable)

        for datatype_name in self.__data_types:

            DataTypes.create(name=datatype_name)

        for name, start, period, unit, data_type, desc in self.__tags:

            Tags.create(
                name=name, 
                start=start, 
                period=period, 
                unit=unit, 
                data_type=data_type,
                desc=desc)

        result = Tags.read_all()


        self.assertEqual(len(result['data']), len(self.__tags))


if __name__=='__main__':

    unittest.main()