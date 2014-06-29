"""
"""
import unittest

import json

import datetime

from freezegun import freeze_time

from flask import Flask

from flask.ext.restful import fields, marshal
from flask.ext.restful.fields import MarshallingException

from acmapi.fields import Date
from acmapi.fields import root_fields
from acmapi.fields import event_fields
from acmapi.fields import post_fields
from acmapi.fields import person_fields
from acmapi.fields import membership_fields
from acmapi.fields import officership_fields

import acmapi

from acmapi import models
from acmapi import resources
from acmapi import DB

from acmapi.resources import API
from acmapi.models import Person
from acmapi.models import Officership

import  base64

HEADERS={
     'Authorization': 'Basic ' + base64.b64encode("root:1234")
     }

class test_officerships_resource(unittest.TestCase):

    @freeze_time("2012-01-14 12:00:01")
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

            officership = Officership.create(
                person = person,
                title = 'Vice Chair',        
                start_date = datetime.date.today(),
                end_date = None,
            )

            DB.session.add(person)
            DB.session.add(officership)
            DB.session.commit()


    @freeze_time("2012-01-14 12:00:01")
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
                    'id': 2,
                    'title': 'foo',
                    'person_id': 2,
                    'person': 'http://localhost:5000/people/2',
                    'start_date': '2014-04-11',
                    'end_date': '2014-04-12',
                })

    @freeze_time("2012-01-14 12:00:01")
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
                {'exception': 'ValueError',
                 'message': 'start_date must be less than end_date'})

    @freeze_time("2012-01-14 12:00:01")
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
                'http://localhost:5000/officerships/2',
                headers = HEADERS)
        
            self.assertEqual(
                json.loads(response.data),
                {'message': 'delete successful'})

            response = client.get(
                'http://localhost:5000/officerships/')
            self.assertEqual(
                json.loads(response.data),
                {
                    'page': 1,
                    'pagesize': 10,
                    'nextpage': None,
                    'officerships': [
                        {
                            'id': 1,
                            'person_id': 1,
                            'person': 'http://localhost:5000/people/1',
                            'title': 'Vice Chair',
                            'start_date': '2012-01-14',
                            'end_date': None,
                        }
                    ]
                })

    @freeze_time("2012-01-14 12:00:01")
    def test_delete_non_existing_officership(self):
        
        with self.app.test_client() as client:

            response = client.delete(
                'http://localhost:5000/officerships/2',
                headers = HEADERS)
        
            self.assertEqual(
                json.loads(response.data),
                { 'exception': 'LookupError',
                  'message': 'officership not found'})

    @freeze_time("2012-01-14 12:00:01")
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
                {
                    'page': 1,
                    'pagesize': 10,
                    'nextpage': None,
                    'officerships': [
                        {
                            'id': 1,
                            'title': 'Vice Chair',
                            'person_id': 1,
                            'person': 'http://localhost:5000/people/1',
                            'start_date': '2012-01-14',
                            'end_date': None,
                            },{
                            'id': 2,
                            'title': 'foo',
                            'person_id': 2,
                            'person': 'http://localhost:5000/people/2',
                            'start_date': '2014-04-11',
                            'end_date': '2014-04-12',
                        }
                    ]
                })

    @freeze_time("2012-01-14 12:00:01")
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
                'http://localhost:5000/officerships/2',
                headers = HEADERS,
                data  = {
                    'start_date': '2014-04-12',
                    'end_date': '2014-04-13',
                })

            self.assertEqual(
                json.loads(response.data),
                {'end_date': '2014-04-13',
                 'id': 2,
                 'person': 'http://localhost:5000/people/2',
                 'person_id': 2,
                 'title': 'foo',
                 'start_date': '2014-04-12'})


    @freeze_time("2012-01-14 12:00:01")
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
                'http://localhost:5000/officerships/2',
                headers = HEADERS,
                data  = {
                    'start_date': '2014-04-13',
                    'end_date': '2014-04-12',
                })

            self.assertEqual(
                json.loads(response.data),
                {'exception': 'ValueError',
                 'message': 'start_date must be less than end_date'})

    @freeze_time("2012-01-14 12:00:01")
    def test_update_non_existing_officership(self):
        
        with self.app.test_client() as client:
            
            response = client.put(
                'http://localhost:5000/officerships/2',
                headers = HEADERS,
                data  = {
                    'start_date': '2014-04-12',
                    'end_date': '2014-04-13',
                })

            self.assertEqual(
                json.loads(response.data),
                { 'exception': 'LookupError',
                  'message': 'officership not found'})
