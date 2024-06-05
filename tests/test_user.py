#!/usr/bin/python3
""" Unittests for HBnB Evolution Part 1 """

import unittest
from models.user import User

class TestCity(unittest.TestCase):
    """Test that the models works as expected
    """

    def test_create_user(self):
        """Tests creation of User instances """

        # don't forget to include the TESTING = 1 flag at the command line
        # type in the terminal: TESTING=1 python3 -m unittest discover
        u = User(first_name="Peter", last_name="Parker", email="iluvspiderman@dailybugle.com", password="123321")

        self.assertIsNotNone(u)

    def test_create_user_invalid_email(self):
        """ Tests error handling during creation of User instances """

        error = 0
        try:
            # invalid characters
            User(first_name="@#$%^&")
        except ValueError:
            error = 1

        # We're not able to use self.assertRaises here since it can't take kwargs
        self.assertEqual(error, 1)

    def test_create_user_invalid_password(self):
        """ Tests error handling during creation of City instances """

        error = 0
        try:
            # password is too short
            User(password="123")
        except ValueError:
            error = 1

        # We're not able to use self.assertRaises here since it can't take kwargs
        self.assertEqual(error, 1)


    # TODO: add more tests

if __name__ == '__main__':
    unittest.main()
