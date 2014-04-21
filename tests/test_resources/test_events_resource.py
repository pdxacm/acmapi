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

from acmapi import database
from acmapi.database import DB

from acmapi import resources
from acmapi.resources import API


class test_memberships_resource(unittest.TestCase):

    def setUp(self):

        self.app = acmapi.create_app(SQLALCHEMY_DATABASE_URI='sqlite://')
        self.app.testing = True

    @freeze_time("2012-01-14 12:00:01")
    def test_add_valid_event(self):
        self.maxDiff = None 
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

            response = client.post(
                'http://localhost:5000/events/',
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    'start': '2014-10-10 10:10:10.00000',
                    'end': '2014-10-10 11:10:10.00000',
                })

            self.assertEqual(
                json.loads(response.data),
                {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                    "editor": "http://localhost:5000/people/1", 
                    "editor_id": 1, 
                    "hidden": False, 
                    "canceled": False, 
                    "event_id": 1, 
                    "revision": 1, 
                    'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                    'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                })

    @freeze_time("2012-01-14 12:00:01")
    def test_edit_valid_event(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

            response = client.post(
                'http://localhost:5000/events/',
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    'start': '2014-10-10 10:10:10.00000',
                    'end': '2014-10-10 11:10:10.00000',
                })

            response = client.post(
                'http://localhost:5000/events/1',
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
                    "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                    "editor": "http://localhost:5000/people/1", 
                    "editor_id": 1, 
                    "hidden": False, 
                    "canceled": False, 
                    "event_id": 1, 
                    "revision": 2, 
                    'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                    'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
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
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 1, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                    },{
                        'title': 'Title B',
                        'description': 'Description B',
                        'location': 'Location B',
                        'speaker': 'Speaker B',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 2, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                    }
                ])

    @freeze_time("2012-01-14 12:00:01")
    def test_multiple_events_with_multiple_revisions(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

            response = client.post(
                'http://localhost:5000/events/',
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'location': 'Location A',
                    'speaker': 'Speaker A',
                    'start': '2014-10-10 10:10:10.00000',
                    'end': '2014-10-10 11:10:10.00000',
                })

            response = client.post(
                'http://localhost:5000/events/1',
                data  = {
                    'title': 'Title B',
                    'description': 'Description B',
                    'location': 'Location B',
                    'speaker': 'Speaker B',
                })

            response = client.post(
                'http://localhost:5000/events/',
                data  = {
                    'title': 'Title C',
                    'description': 'Description C',
                    'location': 'Location C',
                    'speaker': 'Speaker C',
                    'start': '2014-10-10 10:10:10.00000',
                    'end': '2014-10-10 11:10:10.00000',
                })

            response = client.post(
                'http://localhost:5000/events/2',
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
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 1, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                    },{
                        'title': 'Title B',
                        'description': 'Description B',
                        'location': 'Location B',
                        'speaker': 'Speaker B',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 2, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
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
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 2, 
                        "revision": 1, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                    },{
                        'title': 'Title D',
                        'description': 'Description D',
                        'location': 'Location D',
                        'speaker': 'Speaker D',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 2, 
                        "revision": 2, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
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
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 1, 
                        "revision": 2, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                    },{
                        'title': 'Title D',
                        'description': 'Description D',
                        'location': 'Location D',
                        'speaker': 'Speaker D',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "canceled": False, 
                        "event_id": 2, 
                        "revision": 2, 
                        'start': 'Fri, 10 Oct 2014 10:10:10 -0000',
                        'end': 'Fri, 10 Oct 2014 11:10:10 -0000',
                    }
                ])
