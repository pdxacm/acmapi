import unittest


import json

import datetime

from flask import Flask
from flask.ext import restful
from flask.ext.restful import marshal
from flask.ext.restful.fields import Integer

from acmapi import API
from acmapi.field_types import UrlWithParams

class test_urlwithparams_field_type(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    def test_valid_list(self):

        field_1 = {
            'resources': UrlWithParams(
                'resources1', params=['foo'], absolute=True),
            'foo': Integer,
        }

        class Resource1(restful.Resource):
            def get(self):
                return marshal({'foo': 1}, field_1)

        API.add_resource(
            Resource1, 
            '/resources1/', 
            endpoint='resources1')

        API.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources1/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                   'resources': 'http://localhost:5000/resources1/?foo=1',
                   'foo': 1,
               })

    def test_valid_dict(self):

        field_2 = {
            'resources': UrlWithParams(
                'resources2', params={'foo': 'bar'}, absolute=True),
            'bar': Integer,
        }

        class Resource2(restful.Resource):
            def get(self):
                return marshal({'bar': 2}, field_2)

        API.add_resource(
            Resource2, 
            '/resources2/', 
            endpoint='resources2')

        API.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources2/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                   'resources': 'http://localhost:5000/resources2/?foo=2',
                   'bar': 2,
               })

    def test_valid_none(self):

        field_3 = {
            'resources': UrlWithParams(
                'resources3', absolute=True),
        }

        class Resource3(restful.Resource):
            def get(self):
                return marshal({'bar': 3}, field_3)

        API.add_resource(
            Resource3, 
            '/resources3/', 
            endpoint='resources3')

        API.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources3/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                   'resources': 'http://localhost:5000/resources3/',
               })
