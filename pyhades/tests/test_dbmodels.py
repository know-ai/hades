import unittest
from pyhades import PyHades
from pyhades.dbmodels import Units, Variables, DataTypes


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

        for variable_name in self.__variables:

            Variables.create(name=variable_name)

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

        for name, variable in self.__units:

            Units.create(name=name, variable=variable)

        result = Units.read_all()

        self.assertEqual(len(result['data']), len(self.__units))

    def testCountDataTypesAdded(self):

        for datatype_name in self.__data_types:

            DataTypes.create(name=datatype_name)

        result = DataTypes.read_all()

        self.assertEqual(len(result['data']), len(self.__data_types))


if __name__=='__main__':

    unittest.main()