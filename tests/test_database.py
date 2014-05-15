#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright © 2014 Cameron Brandon White

from flask import Flask
from acmapi import DB
from acmapi.models import \
    Event, Post, Person, Membership, Officership
import unittest
import os
import datetime

from flask.ext.sqlalchemy import *

class test_database(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        DB.init_app(self.app)

    def tearDown(self):
        pass

    def test_make_tables(self):
        with self.app.test_request_context():
            DB.create_all()
    
    def test_create_person(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )
            
            self.assertEqual(
                person.id,
                None)
            
            self.assertEqual(
                repr(person),
                '<Person(None)>')

            DB.session.add(person)

            DB.session.commit()

            self.assertEqual(
                person.id,
                1)
            
            self.assertEqual(
                repr(person),
                '<Person(1)>')

            self.assertEqual(
                person.name,
                'John Doe')

            self.assertEqual(
                person.username,
                'johnd')

            self.assertEqual(
                person.email,
                'johnd@example.com')

            self.assertEqual(
                person.website,
                'http://johnd.com')

            DB.session.delete(person)

            DB.session.commit()

    def test_create_person_with_null_username(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = None,
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )
            
            self.assertEqual(
                person.id,
                None)
            
            self.assertEqual(
                repr(person),
                '<Person(None)>')

            DB.session.add(person)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_two_unique_person(self):
        with self.app.test_request_context():

            DB.create_all()

            person1 = Person.create(
                name = 'John Doe',
                username = 'username',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )
            
            person2 = Person.create(
                name = 'John Doe',
                username = 'username',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            DB.session.add(person1)
            DB.session.add(person2)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_two_non_unique_person(self):
        with self.app.test_request_context():

            DB.create_all()

            person1 = Person.create(
                name = 'John Doe',
                username = 'username1',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )
            
            person2 = Person.create(
                name = 'John Doe',
                username = 'username2',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            DB.session.add(person1)
            DB.session.add(person2)
            DB.session.commit()

            self.assertEqual(
                person1.id,
                1)

            self.assertEqual(
                person2.id,
                2)

    def test_create_membership_with_null_end_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            membership = Membership.create(
                person = person,
                start_date = datetime.date.today(),
                end_date = None,
            )

            DB.session.add(membership)

            DB.session.commit()

            self.assertEqual(
                membership.id,
                1)
            
            self.assertEqual(
                repr(membership),
                '<Membership(1)>')

            DB.session.delete(membership)

            DB.session.commit()

    def test_create_membership_with_valid_end_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            membership = Membership.create(
                person = person,
                start_date = datetime.date(2000,1,1),
                end_date = datetime.date(2000,1,2),
            )

            DB.session.add(membership)

            DB.session.commit()

            self.assertEqual(
                membership.id,
                1)
            
            self.assertEqual(
                repr(membership),
                '<Membership(1)>')

            DB.session.delete(membership)

            DB.session.commit()

    def test_create_membership_with_invalid_end_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            membership = Membership.create(
                person = person,
                start_date = datetime.date(2000,1,1),
                end_date = datetime.date(2000,1,1),
            )

            DB.session.add(membership)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_membership_with_null_person(self):
        with self.app.test_request_context():

            DB.create_all()

            membership = Membership.create(
                person = None,
                start_date = datetime.date(2000,1,1),
                end_date = datetime.date(2000,1,2),
            )

            DB.session.add(membership)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_membership_with_null_start_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            membership = Membership.create(
                person = person,
                start_date = None,
                end_date = datetime.date(2000,1,2),
            )

            DB.session.add(membership)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_officership_with_no_end_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            officership = Officership.create(
                person = person,
                title = 'Vice Chair',        
                start_date = datetime.date.today(),
                end_date = None,
            )

            DB.session.add(officership)

            DB.session.commit()

            self.assertEqual(
                officership.id,
                1)
            
            self.assertEqual(
                repr(officership),
                '<Officership(1)>')

            DB.session.delete(officership)

            DB.session.commit()

    def test_create_officership_with_valid_end_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            officership = Officership.create(
                person = person,
                title = 'Vice Chair',        
                start_date = datetime.date(2000,1,2),
                end_date = datetime.date(2000,1,3),
            )

            DB.session.add(officership)

            DB.session.commit()

            self.assertEqual(
                officership.id,
                1)
            
            self.assertEqual(
                repr(officership),
                '<Officership(1)>')

            DB.session.delete(officership)

            DB.session.commit()

    def test_create_officership_with_invalid_end_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            officership = Officership.create(
                person = person,
                title = 'Vice Chair',        
                start_date = datetime.date(2000,1,2),
                end_date = datetime.date(2000,1,2),
            )

            DB.session.add(officership)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_officership_with_null_start_date(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            officership = Officership.create(
                person = person,
                title = 'Vice Chair',        
                start_date = None,
                end_date = datetime.date(2000,1,2),
            )

            DB.session.add(officership)
            
            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_officership_with_null_title(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            officership = Officership.create(
                person = person,
                title = None,        
                start_date = datetime.date(2000,1,2),
                end_date = datetime.date(2000,1,3),
            )

            DB.session.add(officership)
            
            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_officership_with_null_person(self):
        with self.app.test_request_context():

            DB.create_all()

            officership = Officership.create(
                person = None,
                title = 'Vice Chair',        
                start_date = datetime.date(2000,1,2),
                end_date = datetime.date(2000,1,3),
            )

            DB.session.add(officership)
            
            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_event(self):
         with self.app.test_request_context():

            DB.create_all()
             
            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime.today(),
                end = datetime.datetime.today(),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(person)

            DB.session.add(event)

            DB.session.commit()

            DB.session.delete(event)

            DB.session.commit()

    def test_create_event_with_null_person(self):
         with self.app.test_request_context():

            DB.create_all()
             
            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = None,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime.today(),
                end = datetime.datetime.today(),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )


            DB.session.add(event)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_event_with_start_before_end(self):
         with self.app.test_request_context():

            DB.create_all()
             
            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,2),
                end = datetime.datetime(2000,1,3),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(person)

            DB.session.add(event)

            DB.session.commit()

            DB.session.delete(event)

            DB.session.commit()

    def test_create_event_with_start_equals_end(self):
         with self.app.test_request_context():

            DB.create_all()
             
            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,2),
                end = datetime.datetime(2000,1,2),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(person)

            DB.session.add(event)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_event_with_start_after_end(self):
         with self.app.test_request_context():

            DB.create_all()
             
            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,3),
                end = datetime.datetime(200,1,2),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(person)

            DB.session.add(event)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_two_unique_events(self):
         with self.app.test_request_context():

            DB.create_all()
             
            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            DB.session.add(person)

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,2),
                end = datetime.datetime(2000,1,3),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(event)

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,2),
                end = datetime.datetime(2000,1,3),
                canceled = False,
                hidden = False,
                list = 0,
                index = 1,
            )

            DB.session.add(event)

            DB.session.commit()

    def test_create_two_non_unique_events(self):
         with self.app.test_request_context():

            DB.create_all()
             
            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            DB.session.add(person)

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,2),
                end = datetime.datetime(2000,1,3),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(event)

            event = Event.create(
                title = "Event 1",
                description = "This is Event 1",
                speaker = "By the Event 1 speaker",
                location = "In the Event Room",
                editor = person,
                edited_datetime = datetime.datetime.today(),
                start = datetime.datetime(2000,1,2),
                end = datetime.datetime(2000,1,3),
                canceled = False,
                hidden = False,
                list = 0,
                index = 0,
            )

            DB.session.add(event)

            try:
                DB.session.commit()
            except Exception:
                pass
            else:
                raise Exception("IntegrityError excepted but not thrown")

    def test_create_post(self):
        with self.app.test_request_context():

            DB.create_all()

            person = Person.create(
                name = 'John Doe',
                username = 'johnd',
                email = 'johnd@example.com',
                website = 'http://johnd.com',
            )

            DB.session.add(person)
             
            post = Post.create(
                title = 'Post 1',
                description = 'This is Post 1',
                content = 'This is Post 1 content',
                editor = person,
                edited_datetime = datetime.datetime.today(),
                hidden = False,
                list = 0,
                index = 0,
             )

            DB.session.add(post)
     
            DB.session.commit()

            DB.session.delete(post)

            DB.session.commit()
