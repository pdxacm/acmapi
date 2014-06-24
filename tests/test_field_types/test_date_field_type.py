import unittest

import json

from datetime import datetime

from flask import Flask
from flask.ext.restful import marshal

from acmapi.field_types import Date

from freezegun import freeze_time

DATE_FORMAT = '%Y-%m-%d'

class test_date_field_type(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    @freeze_time("2012-01-14 12:00:01")
    def test_valid(self):
        
        field = {
            'date': Date(DATE_FORMAT),
        }

        with self.app.test_request_context():

            self.assertEqual(
                dict(marshal({'date': datetime.now()}, field)),
                {'date': "2012-01-14"})
