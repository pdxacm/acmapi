"""
"""
import unittest
from freezegun import freeze_time

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
from acmapi.models import Person, Officership

import  base64

HEADERS={
     'Authorization': 'Basic ' + base64.b64encode("root:1234")
     }

class test_memberships_resource(unittest.TestCase):

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
    def test_add_valid_event(self):
        self.maxDiff = None 
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
                'http://localhost:5000/events/',
                headers = HEADERS,
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    'start': '2014-10-10 10:10:10.000000',
                    'end': '2014-10-10 11:10:10.000000',
                })

            self.assertEqual(
                json.loads(response.data),
                {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    "edited_at": '2012-01-14 12:00:01.000000',
                    "editor": "http://localhost:5000/people/1", 
                    "editor_id": 1, 
                    "hidden": False, 
                    "canceled": False, 
                    "event_id": 1, 
                    "revision": 1, 
                    'start': '2014-10-10 10:10:10.000000',
                    'end': '2014-10-10 11:10:10.000000',
                })

    @freeze_time("2012-01-14 12:00:01")
    def test_edit_valid_event(self):
        
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
                'http://localhost:5000/events/',
                headers = HEADERS,
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    'start': '2014-10-10 10:10:10.000000',
                    'end': '2014-10-10 11:10:10.000000',
                })

            response = client.put(
                'http://localhost:5000/events/1',
                headers = HEADERS,
                data  = {
                    'title': 'Title B',
                    'description': 'Description B',
                    'location': 'Location B',
                    'speaker': 'Speaker B',
                })

            self.assertEqual(
                json.loads(response.data),
                {
                    'title': 'Title B',
                    'description': 'Description B',
                    'location': 'Location B',
                    'speaker': 'Speaker B',
                    "edited_at": '2012-01-14 12:00:01.000000',
                    "editor": "http://localhost:5000/people/1", 
                    "editor_id": 1, 
                    "hidden": False, 
                    "canceled": False, 
                    "event_id": 1, 
                    "revision": 2, 
                    'start': '2014-10-10 10:10:10.000000',
                    'end': '2014-10-10 11:10:10.000000',
                })

            response = client.get(
                'http://localhost:5000/events/1')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title A',
                        'description': 'Description A',
                        'location': 'Location A',
                        'speaker': 'Speaker A',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 1, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    },{
                        'title': 'Title B',
                        'description': 'Description B',
                        'location': 'Location B',
                        'speaker': 'Speaker B',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 2, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    }
                ])

    @freeze_time("2012-01-14 12:00:01")
    def test_multiple_events_with_multiple_revisions(self):
        
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
                'http://localhost:5000/events/',
                headers = HEADERS,
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    'start': '2014-10-10 10:10:10.000000',
                    'end': '2014-10-10 11:10:10.000000',
                })

            response = client.put(
                'http://localhost:5000/events/1',
                headers = HEADERS,
                data  = {
                    'title': 'Title B',
                    'description': 'Description B',
                    'location': 'Location B',
                    'speaker': 'Speaker B',
                })

            response = client.post(
                'http://localhost:5000/events/',
                headers = HEADERS,
                data  = {
                    'title': 'Title C',
                    'description': 'Description C',
                    'location': 'Location C',
                    'speaker': 'Speaker C',
                    'start': '2014-10-10 10:10:10.000000',
                    'end': '2014-10-10 11:10:10.000000',
                })

            response = client.put(
                'http://localhost:5000/events/2',
                headers = HEADERS,
                data  = {
                    'title': 'Title D',
                    'description': 'Description D',
                    'location': 'Location D',
                    'speaker': 'Speaker D',
                })

            response = client.get(
                'http://localhost:5000/events/1')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title A',
                        'description': 'Description A',
                        'location': 'Location A',
                        'speaker': 'Speaker A',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 1, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    },{
                        'title': 'Title B',
                        'description': 'Description B',
                        'location': 'Location B',
                        'speaker': 'Speaker B',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 2, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    }
                ])

            response = client.get(
                'http://localhost:5000/events/2')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title C',
                        'description': 'Description C',
                        'location': 'Location C',
                        'speaker': 'Speaker C',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 2, 
                        "revision": 1, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    },{
                        'title': 'Title D',
                        'description': 'Description D',
                        'location': 'Location D',
                        'speaker': 'Speaker D',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 2, 
                        "revision": 2, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    }
                ])

            response = client.get(
                'http://localhost:5000/events/')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title B',
                        'description': 'Description B',
                        'location': 'Location B',
                        'speaker': 'Speaker B',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 2, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    },{
                        'title': 'Title D',
                        'description': 'Description D',
                        'location': 'Location D',
                        'speaker': 'Speaker D',
                        "edited_at": '2012-01-14 12:00:01.000000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 2, 
                        "revision": 2, 
                        'start': '2014-10-10 10:10:10.000000',
                        'end': '2014-10-10 11:10:10.000000',
                    }
                ])
