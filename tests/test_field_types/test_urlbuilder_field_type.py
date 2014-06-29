import unittest

import json

import datetime

from flask import Flask
from flask.ext import restful
from flask.ext.restful import marshal

from acmapi import API
from acmapi.field_types import UrlBuilder

class test_urlbuilder_field_type(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = restful.Api()

    def test_none(self):

        field = {
            'resources0': UrlBuilder,
        }

        class Resource0(restful.Resource):
            def get(self):
                return marshal({ 'resources0':{}
                    }, field)

        self.api.add_resource(
            Resource0, 
            '/resources0/', 
            endpoint='resources0')

        self.api.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources0/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                    'resources0': None,
               })


    def test_non_none_endpoint(self):

        field = {
            'resources1': UrlBuilder,
        }

        class Resource1(restful.Resource):
            def get(self):
                return marshal({ 
                    'resources1': {
                        'endpoint': 'resources1'}
                    }, field)

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
                    'resources1': 'http://localhost:5000/resources1/',
               })

    def test_none_endpoint(self):

        field = {
            'resources2': UrlBuilder,
        }

        class Resource2(restful.Resource):
            def get(self):
                return marshal({ 
                    'resources2': {
                        'endpoint': None}
                    }, field)

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
                    'resources2': None,
               })

    def test_non_none_endpoint_with_params(self):

        field = {
            'resources3': UrlBuilder,
        }

        class Resource3(restful.Resource):
            def get(self):
                return marshal({ 
                    'resources3': {
                        'endpoint': 'resources3',
                        'params': {
                            'foo': 1,
                            'bar': 2}
                        }
                    }, field)

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
                    'resources3': 'http://localhost:5000/resources3/?foo=1&bar=2',
               })

    def test_none_endpoint_with_params(self):

        field = {
            'resources4': UrlBuilder,
        }

        class Resource4(restful.Resource):
            def get(self):
                return marshal({ 
                    'resources4': {
                        'endpoint': None,
                        'params': {
                            'foo': 1,
                            'bar': 2}
                        }
                    }, field)

        API.add_resource(
            Resource4, 
            '/resources4/', 
            endpoint='resources4')

        API.init_app(self.app)
            
        with self.app.test_client() as client:

            response = client.get('http://localhost:5000/resources4/')
        
            self.assertEqual(
                    response.status,
                    '200 OK')
            
            self.assertEqual(
               json.loads(response.data),
               {
                    'resources4': None,
               })
