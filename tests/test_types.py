import unittest
import datetime

from acmapi.types import date_type
from acmapi.types import datetime_type
from acmapi.types import ValidationError

class test_date_type(unittest.TestCase):
    
    def test_valid_date(self):
        self.assertEqual(
            date_type('2014-04-11'),
            datetime.date(2014, 4, 11))

    def test_invalid_date(self):
        try:
            date_type('2014-04-31')
        except ValidationError:
            pass
        else:
            raise Exception('ValidationError was excepted')

    def test_invalid_argument(self):

        try:
            date_type(1)
        except TypeError:
            pass
        else:
            raise Exception('ValidationError was excepted')

class test_datetime_type(unittest.TestCase):

    def test_valid_datetime(self):
        self.assertEqual(
            datetime_type('2014-04-11 16:20:00.00000'),
            datetime.datetime(2014, 4, 11, 16, 20))

    def test_invalid_datetime(self):
        try:
            datetime_type('2014-04-31')
        except ValidationError:
            pass
        else:
            raise Exception('ValidationError was excepted')

    def test_invalid_argument(self):

        try:
            datetime_type(1)
        except TypeError:
            pass
        else:
            raise Exception('ValidationError was excepted')
