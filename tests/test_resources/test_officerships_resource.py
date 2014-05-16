"""
"""
import unittest

import json

import datetime

from flask import Flask

from flask.ext.restful import fields, marshal

from acmapi.fields import \
    DateField, MarshallingException, \
    root_fields, event_fields, post_fields, person_fields, \
    membership_fields, officership_fields

import acmapi

from acmapi import models, resources, DB
from acmapi.resources import API
from acmapi.models import Person

import  base64

HEADERS={
     'Authorization': 'Basic ' + base64.b64encode("root:1234")
     }

class test_officerships_resource(unittest.TestCase):

    def setUp(self):

        self.app = acmapi.create_app(SQLALCHEMY_DATABASE_URI='sqlite://')
        self.app.testing = True

        with self.app.test_request_context():
            DB.create_all()
            person = Person.create(
                name = None,
                username = 'root',
                email = None,
                website = None,
                password = '1234',
            )
            DB.session.add(person)
            DB.session.commit()


    def test_add_valid_membership(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                headers = HEADERS,
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/officerships/',
                headers = HEADERS,
                data  = {
                    'person_id': 2,
                    'title': 'foo',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'id': 1,
                    'title': 'foo',
                    'person_id': 2,
                    'person': 'http://localhost:5000/people/2',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })

    def test_add_invalid_officership(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                headers = HEADERS,
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/officerships/',
                headers = HEADERS,
                data  = {
                    'person_id': 2,
                    'title': 'foo',
                    'start_date': '2014-04-13',
                    'end_date': '2014-04-12',
                })
        
            self.assertEqual(
                json.loads(response.data),
                {'message': 'start_date must be less than end_date'})

    def test_delete_existing_officership(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                headers = HEADERS,
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/officerships/',
                headers = HEADERS,
                data  = {
                    'person_id': 2,
                    'title': 'foo',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })

            response = client.delete(
                'http://localhost:5000/officerships/1',
                headers = HEADERS)
        
            self.assertEqual(
                json.loads(response.data),
                {'message': 'delete successful'})

            response = client.get(
                'http://localhost:5000/officerships/')
            self.assertEqual(
                json.loads(response.data),
                [])

    def test_delete_non_existing_officership(self):
        
        with self.app.test_client() as client:

            response = client.delete(
                'http://localhost:5000/officerships/1',
                headers = HEADERS)
        
            self.assertEqual(
                json.loads(response.data),
                {'message': 'delete failed, officership not found'})

    def test_list_all_officerships_1(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                headers = HEADERS,
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/officerships/',
                headers = HEADERS,
                data  = {
                    'person_id': 2,
                    'title': 'foo',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })


            response = client.get(
                'http://localhost:5000/officerships/')
            self.assertEqual(
                json.loads(response.data),
                [{
                    'id': 1,
                    'title': 'foo',
                    'person_id': 2,
                    'person': 'http://localhost:5000/people/2',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                }])

    def test_update_existing_officership(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                headers = HEADERS,
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/officerships/',
                headers = HEADERS,
                data  = {
                    'person_id': 2,
                    'title': 'foo',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })

            response = client.put(
                'http://localhost:5000/officerships/1',
                headers = HEADERS,
                data  = {
                    'start_date': '2014-04-12',
                    'end_date': '2014-04-13',
                })

            self.assertEqual(
                json.loads(response.data),
                {'message': 'officership update successful'})

    def test_update_existing_officership_invalid(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                headers = HEADERS,
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/officerships/',
                headers = HEADERS,
                data  = {
                    'person_id': 2,
                    'title': 'foo',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })

            response = client.put(
                'http://localhost:5000/officerships/1',
                headers = HEADERS,
                data  = {
                    'start_date': '2014-04-13',
                    'end_date': '2014-04-12',
                })

            self.assertEqual(
                json.loads(response.data),
                {'message': 'start_date must be less than end_date'})

    def test_update_non_existing_officership(self):
        
        with self.app.test_client() as client:
            
            response = client.put(
                'http://localhost:5000/officerships/1',
                headers = HEADERS,
                data  = {
                    'start_date': '2014-04-12',
                    'end_date': '2014-04-13',
                })

            self.assertEqual(
                json.loads(response.data),
                {'message': 'officership not found'})
