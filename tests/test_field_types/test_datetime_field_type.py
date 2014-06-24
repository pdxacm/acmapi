import unittest

import json

from datetime import datetime

from flask import Flask
from flask.ext.restful import marshal
from flask.ext.restful.fields import MarshallingException

from acmapi.field_types import DateTime

from freezegun import freeze_time


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

class test_date_field_type(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    @freeze_time("2012-01-14 12:00:01")
    def test_valid(self):
        
        field = {
            'date': DateTime(DATETIME_FORMAT),
        }

        with self.app.test_request_context():

            self.assertEqual(
                dict(marshal({'date': datetime.now()}, field)),
                {'date': "2012-01-14 12:00:01.000000"})
