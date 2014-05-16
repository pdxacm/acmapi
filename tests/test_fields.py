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

from acmapi import models
from acmapi.models import DB

from acmapi import resources
from acmapi.resources import API

class test_fields(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

        self.app.testing = True
        
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        
        DB.init_app(self.app)
        
        API.init_app(self.app)

    def test_root_fields(self):
        with self.app.test_client() as client:
            with self.app.test_request_context():
                self.assertEqual(
                    dict(marshal({}, root_fields)),
                    {
                        "events_url": [
                            "http://localhost/events/",
                            "http://localhost/events/<int:event_id>"
                        ], 
                        "memberships_url": [
                            "http://localhost/memberships/",
                            "http://localhost/memberships/<int:membership_id>"
                        ], 
                        "officerships_url": [
                            "http://localhost/officerships/",
                            "http://localhost/officerships/<int:officership_id>"
                        ], 
                        "people_url": [
                            "http://localhost/people/", 
                            "http://localhost/people/<int:person_id>", 
                            "http://localhost/people/<int:editor_id>",
                            "http://localhost/people/<string:username>"
                        ], 
                        "posts_url": [
                            "http://localhost/posts/",
                            "http://localhost/posts/<int:post_id>"
                        ]
                    })
    
    def test_person_fields(self):
        
        with self.app.test_client() as client:
            with self.app.test_request_context():

                DB.create_all()

                person = models.Person.create(
                    name = 'John Doe',
                    username = 'johnd',
                    email = 'johnd@example.com',
                    website = 'http://johnd.com',
                    password = 'password1234',
                )
                
                DB.session.add(person)
                DB.session.commit()

                self.assertEqual(
                    dict(marshal(person, person_fields)),
                    {"id": 1, "username": u"johnd", "email":
                        u"johnd@example.com", "website":
                        u"http://johnd.com", 'name': u'John Doe'})

    def test_event_fields(self):
        
        with self.app.test_client() as client:
            with self.app.test_request_context():

                DB.create_all()
                 
                person = models.Person.create(
                    name = 'John Doe',
                    username = 'johnd',
                    email = 'johnd@example.com',
                    website = 'http://johnd.com',
                    password = 'password1234',
                )

                event = models.Event.create(
                    title = "Event 1",
                    description = "This is Event 1",
                    speaker = "By the Event 1 speaker",
                    location = "In the Event Room",
                    editor = person,
                    edited_datetime = 
                        datetime.datetime(2014, 4, 15, 21, 20, 30),
                    start =
                        datetime.datetime(2014, 4, 15, 21, 20, 30),
                    end =
                        datetime.datetime(2014, 4, 16, 21, 20, 30),
                    canceled = False,
                    hidden = False,
                    list = 0,
                    index = 0,
                )

                DB.session.add(person)

                DB.session.add(event)

                DB.session.commit()
                DB.create_all()

                self.assertEqual(
                    dict(marshal(event, event_fields)),
                    {'event_id': 0, 'description': u'This is Event 1',
                    'location': u'In the Event Room', 
                    'speaker': u'By the Event 1 speaker',
                    'title': u'Event 1', 'canceled': False,
                    'hidden': False, 
                    'start': 'Tue, 15 Apr 2014 21:20:30 -0000',
                    'end': 'Wed, 16 Apr 2014 21:20:30 -0000',
                    'revision': 0, 
                    'edited_at': 'Tue, 15 Apr 2014 21:20:30 -0000',
                    'editor_id': 1,
                    'editor': 'http://localhost/people/1'})
        
    def test_post_fields(self):
        
        with self.app.test_client() as client:
            with self.app.test_request_context():

                DB.create_all()

                person = models.Person.create(
                    name = 'John Doe',
                    username = 'johnd',
                    email = 'johnd@example.com',
                    website = 'http://johnd.com',
                    password = 'password1234',
                )

                DB.session.add(person)
                 
                post = models.Post.create(
                    title = 'Post 1',
                    description = 'This is Post 1',
                    content = 'This is Post 1 content',
                    editor = person,
                    edited_datetime = 
                        datetime.datetime(2014, 4, 15, 21, 20, 30),
                    hidden = False,
                    list = 0,
                    index = 0,
                 )

                DB.session.add(post)
         
                DB.session.commit()

                self.assertEqual(
                    dict(marshal(post, post_fields)),
                    {'post_id': 0, 'description': u'This is Post 1',
                    'content': 'This is Post 1 content',
                    'title': u'Post 1', 'hidden': False, 
                    'revision': 0, 
                    'edited_at': 'Tue, 15 Apr 2014 21:20:30 -0000',
                    'editor_id': 1,
                    'editor': 'http://localhost/people/1'})

    def test_membership_fields(self):
        
        with self.app.test_client() as client:
            with self.app.test_request_context():

                DB.create_all()

                person = models.Person.create(
                    name = 'John Doe',
                    username = 'johnd',
                    email = 'johnd@example.com',
                    website = 'http://johnd.com',
                    password = 'password1234',
                )

                DB.session.add(person)

                memberships = models.Membership.create(
                    person = person,
                    start_date = datetime.date(2014, 4, 15),
                    end_date = datetime.date(2014, 4, 16))

                DB.session.add(memberships)

                DB.session.commit()

                self.assertEqual(
                    dict(marshal(memberships, membership_fields)),
                    {'id': 1, 'person_id': 1,
                    'person': 'http://localhost/people/1',
                    'start_date': '2014-04-15',
                    'end_date': '2014-04-16'})

    def test_officership_fields(self):
        
        with self.app.test_client() as client:
            with self.app.test_request_context():

                DB.create_all()

                person = models.Person.create(
                    name = 'John Doe',
                    username = 'johnd',
                    email = 'johnd@example.com',
                    website = 'http://johnd.com',
                    password = 'password1234',
                )

                DB.session.add(person)

                officership = models.Officership.create(
                    person = person,
                    title = 'Vice Chair',        
                    start_date = datetime.date(2014, 4, 15),
                    end_date = datetime.date(2014, 4, 16))

                DB.session.add(officership)

                DB.session.commit()

                self.assertEqual(
                    dict(marshal(officership, officership_fields)),
                    {'id': 1, 'title': u'Vice Chair', 'person_id': 1,
                    'person': 'http://localhost/people/1',
                    'start_date': '2014-04-15',
                    'end_date': '2014-04-16'})
