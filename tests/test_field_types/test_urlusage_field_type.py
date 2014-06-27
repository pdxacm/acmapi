import unittest

import json

import datetime

from flask import Flask
from flask.ext import restful
from flask.ext.restful import marshal

from acmapi import API
from acmapi.field_types import UrlUsage

class test_urlusage_field_type(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = restful.Api()

    def test_valid(self):

        field = {
            'resources': UrlUsage('resources', absolute=True),
        }

        class Resource(restful.Resource):
            def get(self):
                return marshal({}, field)

        self.api.add_resource(
            Resource, 
            '/resources/', 
            endpoint='resources')

        self.api.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                    'resources': [
                        'http://localhost:5000/resources/',
                    ]
               })


