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

from acmapi import models
from acmapi.models import DB

from acmapi import resources
from acmapi.resources import API


class test_memberships_resource(unittest.TestCase):

    def setUp(self):

        self.app = acmapi.create_app(SQLALCHEMY_DATABASE_URI='sqlite://')
        self.app.testing = True

    @freeze_time("2012-01-14 12:00:01")
    def test_add_valid_post(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/posts/',
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'content': 'This is Post 1 content',
                })

            self.assertEqual(
                json.loads(response.data),
                {
                    'title': 'Title A',
                    'description': 'Description A',
                    'content': 'This is Post 1 content',
                    "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                    "editor": "http://localhost:5000/people/1", 
                    "editor_id": 1, 
                    "hidden": False, 
                    "post_id": 1, 
                    "revision": 1, 
                })

    @freeze_time("2012-01-14 12:00:01")
    def test_edit_valid_post(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/posts/',
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'content': 'This is Post 1 content',
                })

            response = client.put(
                'http://localhost:5000/posts/1',
                data  = {
                    'title': 'Title B',
                    'description': 'Description B',
                    'content': 'This is Post 1 content',
                })

            self.assertEqual(
                json.loads(response.data),
                {
                    'title': 'Title B',
                    'description': 'Description B',
                    'content': 'This is Post 1 content',
                    "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                    "editor": "http://localhost:5000/people/1", 
                    "editor_id": 1, 
                    "hidden": False, 
                    "post_id": 1, 
                    "revision": 2, 
                })

            response = client.get(
                'http://localhost:5000/posts/1',
                data  = {
                    'title': 'Title B',
                    'description': 'Description B',
                    'content': 'This is Post 1 content',
                })

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title A',
                        'description': 'Description A',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 1, 
                        "revision": 1, 
                    },{
                        'title': 'Title B',
                        'description': 'Description B',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 1, 
                        "revision": 2, 
                    }
                ])

    @freeze_time("2012-01-14 12:00:01")
    def test_multiple_posts_with_multiple_revisions(self):
        
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                    'password': 'password1234',
                })

            response = client.post(
                'http://localhost:5000/posts/',
                data  = {
                    'title': 'Title A',
                    'description': 'Description A',
                    'content': 'This is Post 1 content',
                })

            response = client.put(
                'http://localhost:5000/posts/1',
                data  = {
                    'title': 'Title B',
                    'description': 'Description B',
                    'content': 'This is Post 1 content',
                })

            response = client.post(
                'http://localhost:5000/posts/',
                data  = {
                    'title': 'Title C',
                    'description': 'Description C',
                    'content': 'This is Post 1 content',
                })

            response = client.put(
                'http://localhost:5000/posts/2',
                data  = {
                    'title': 'Title D',
                    'description': 'Description D',
                    'content': 'This is Post 1 content',
                })

            response = client.get(
                'http://localhost:5000/posts/1')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title A',
                        'description': 'Description A',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 1, 
                        "revision": 1, 
                    },{
                        'title': 'Title B',
                        'description': 'Description B',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 1, 
                        "revision": 2, 
                    }
                ])

            response = client.get(
                'http://localhost:5000/posts/2')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title C',
                        'description': 'Description C',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 2, 
                        "revision": 1, 
                    },{
                        'title': 'Title D',
                        'description': 'Description D',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 2, 
                        "revision": 2, 
                    }
                ])

            response = client.get(
                'http://localhost:5000/posts/')

            self.assertEqual(
                json.loads(response.data),
                [
                    {
                        'title': 'Title B',
                        'description': 'Description B',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 1, 
                        "revision": 2, 
                    },{
                        'title': 'Title D',
                        'description': 'Description D',
                        'content': 'This is Post 1 content',
                        "edited_at": 'Sat, 14 Jan 2012 12:00:01 -0000',
                        "editor": "http://localhost:5000/people/1", 
                        "editor_id": 1, 
                        "hidden": False, 
                        "post_id": 2, 
                        "revision": 2, 
                    }
                ])
