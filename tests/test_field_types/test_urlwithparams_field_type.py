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
        self.api = restful.Api()

    def test_valid_list(self):

        field_1 = {
            'resources': UrlWithParams(
                'resources10', params=['foo'], absolute=True),
            'foo': Integer,
        }

        class Resource10(restful.Resource):
            def get(self):
                return marshal({'foo': 1}, field_1)

        self.api.add_resource(
            Resource10, 
            '/resources10/', 
            endpoint='resources10')

        self.api.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources10/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                   'resources': 'http://localhost:5000/resources10/?foo=1',
                   'foo': 1,
               })

    def test_valid_dict(self):

        field_2 = {
            'resources': UrlWithParams(
                'resources20', params={'foo': 'bar'}, absolute=True),
            'bar': Integer,
        }

        class Resource20(restful.Resource):
            def get(self):
                return marshal({'bar': 2}, field_2)

        API.add_resource(
            Resource20, 
            '/resources20/', 
            endpoint='resources20')

        API.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources20/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                   'resources': 'http://localhost:5000/resources20/?foo=2',
                   'bar': 2,
               })

    def test_valid_none(self):

        field_3 = {
            'resources': UrlWithParams(
                'resources30', absolute=True),
        }

        class Resource30(restful.Resource):
            def get(self):
                return marshal({'bar': 3}, field_3)

        API.add_resource(
            Resource30, 
            '/resources30/', 
            endpoint='resources30')

        API.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources30/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                   'resources': 'http://localhost:5000/resources30/',
               })
