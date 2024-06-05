#!/usr/bin/python3
""" Unittests for HBnB Evolution Part 1 """

# from io import StringIO
# import sys
import os
import unittest
from models.city import City
import data as data

class TestCity(unittest.TestCase):
    """Test that the models works as expected
    """

    def test_create_city(self):
        """Tests creation of City instances """

        # Note that this test only works if the test country data is loaded
        # don't forget to include the TESTING = 1 flag at the command line
        # type in the terminal: TESTING=1 python3 -m unittest discover
        c = City(name="Vancouver", country_id="d291a77f-fa95-4385-b70e-2691df246475")

        self.assertIsNotNone(c)

    def test_create_city_invalid_name(self):
        """ Tests error handling during creation of City instances """

        error = 0
        try:
            City(name="@#$%^&", country_id="d291a77f-fa95-4385-b70e-2691df246475")
        except ValueError:
            error = 1

        # We're not able to use self.assertRaises here since it can't take kwargs
        self.assertEqual(error, 1)

    def test_create_city_invalid_country_id(self):
        """ Tests error handling during creation of City instances """

        error = 0
        try:
            City(name="Wakanda", country_id="616")
        except ValueError:
            error = 1

        # We're not able to use self.assertRaises here since it can't take kwargs
        self.assertEqual(error, 1)


    # TODO: add more tests

if __name__ == '__main__':
    unittest.main()
