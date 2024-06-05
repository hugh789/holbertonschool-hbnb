#!/usr/bin/python3
""" Unittests for HBnB Evolution Part 1 """

# from io import StringIO
# import sys
import os
import unittest
import data as data
from app import app

class TestApp(unittest.TestCase):
    """Test that the app API endpoints work as expected
    """

    # don't forget to include the TESTING = 1 flag at the command line
    # type in the terminal: TESTING=1 python3 -m unittest tests/test_app.py

    @classmethod
    def setUpClass(cls):
        # Set up the Flask test client
        cls.app = app.test_client()
        # cls.app.testing = True

    def test_hello_world(self):
        """ Test the '/' endpoint """
        # Send a GET request to the '/' endpoint
        response = self.app.get('/')

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        expected = "Hello World"
        output = response.get_data(as_text=True)
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
