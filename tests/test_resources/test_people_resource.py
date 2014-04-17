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

from acmapi import database
from acmapi.database import DB

from acmapi import resources
from acmapi.resources import API

class test_people_resource(unittest.TestCase):

    def setUp(self):

        self.app = acmapi.create_app(SQLALCHEMY_DATABASE_URI='sqlite://')
        self.app.testing = True

    def test_add_unique_person(self):
        
        with self.app.test_client() as client:
            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'id': 1,
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

    def test_add_duplicate_person(self):
        
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
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'message': 'username already exists'
                })

    def test_find_existing_person_by_id(self):
        
        with self.app.test_client() as client:
            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })
            
            response = client.get(
                    'http://localhost:5000/people/1')
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'id': 1,
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

    def test_find_existing_person_by_username(self):
        
        with self.app.test_client() as client:
            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })
            
            response = client.get(
                    'http://localhost:5000/people/bob')
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'id': 1,
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

    def test_find_non_existing_person_by_id(self):
        
        with self.app.test_client() as client:
            
            response = client.get(
                    'http://localhost:5000/people/1')
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'message': 'person not found',
                })

    def test_find_non_existing_person_by_username(self):
        
        with self.app.test_client() as client:
            
            response = client.get(
                    'http://localhost:5000/people/bob')
        
            self.assertEqual(
                json.loads(response.data),
                {
                    'message': 'person not found',
                })

    def test_list_everything_0(self):
        with self.app.test_client() as client:
            
            response = client.get(
                    'http://localhost:5000/people/')
        
            self.assertEqual(
                json.loads(response.data), [])

    def test_list_everything_1(self):
        with self.app.test_client() as client:
            
            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

            response = client.get(
                    'http://localhost:5000/people/')
        
            self.assertEqual(
                json.loads(response.data),
                [{
                    'id': 1,
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                }])

    def test_list_everything_2(self):
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
                'http://localhost:5000/people/',
                data  = {
                    'username': 'foo',
                    'name': 'Foo Bar',
                    'email': 'foobar@example.com',
                    'website': 'http://foobar.example.com',
                })

            response = client.get(
                    'http://localhost:5000/people/')
        
            self.assertEqual(
                json.loads(response.data),
                [{
                    'id': 1,
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                },
                {
                    'id': 2,
                    'username': 'foo',
                    'name': 'Foo Bar',
                    'email': 'foobar@example.com',
                    'website': 'http://foobar.example.com',
                }])

    def test_delete_existing_by_id(self):
        with self.app.test_client() as client:
            
            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

            response = client.delete(
                    'http://localhost:5000/people/1')

            self.assertEqual(
                json.loads(response.data),
                { 'message': 'delete successful' })

            response = client.get(
                    'http://localhost:5000/people/')
             
            self.assertEqual(
                json.loads(response.data), [])

    def test_delete_existing_by_username(self):
        with self.app.test_client() as client:
            
            response = client.post(
                'http://localhost:5000/people/',
                data  = {
                    'username': 'bob',
                    'name': 'Bob Billy',
                    'email': 'bbob@example.com',
                    'website': 'http://bbob.example.com',
                })

            response = client.delete(
                    'http://localhost:5000/people/bob')

            self.assertEqual(
                json.loads(response.data),
                { 'message': 'delete successful' })

            response = client.get(
                    'http://localhost:5000/people/')
             
            self.assertEqual(
                json.loads(response.data), [])

    def test_delete_non_existing_by_id(self):
        with self.app.test_client() as client:
            
            response = client.delete(
                    'http://localhost:5000/people/1')

            self.assertEqual(
                json.loads(response.data),
                { 'message': 'delete failed, person not found' })

            response = client.get(
                    'http://localhost:5000/people/')
             
            self.assertEqual(
                json.loads(response.data), [])

    def test_delete_non_existing_by_username(self):
        with self.app.test_client() as client:
            
            response = client.delete(
                    'http://localhost:5000/people/bob')

            self.assertEqual(
                json.loads(response.data),
                { 'message': 'delete failed, person not found' })

            response = client.get(
                    'http://localhost:5000/people/')
             
            self.assertEqual(
                json.loads(response.data), [])

    def test_invalid_delete(self):
        with self.app.test_client() as client:
            
            response = client.delete(
                    'http://localhost:5000/people/')

            self.assertEqual(
                json.loads(response.data),
                { 'message': 'delete failed, nothing to delete' })

            response = client.get(
                    'http://localhost:5000/people/')
             
            self.assertEqual(
                json.loads(response.data), [])

    def test_update_existing_person_by_id(self):
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
                'http://localhost:5000/people/1',
                data  = {
                    'username': 'bob',
                    'name': 'Jim Billy',
                    'email': 'jbob@example.com',
                    'website': 'http://jbob.example.com',
                })
        
            self.assertEqual(
                json.loads(response.data),
                { 'message': 'person update successful' })

            response = client.get(
                'http://localhost:5000/people/1')

            self.assertEqual(
                json.loads(response.data),
                {
                    'id': 1,
                    'username': 'bob',
                    'name': 'Jim Billy',
                    'email': 'jbob@example.com',
                    'website': 'http://jbob.example.com',
                })

    def test_update_existing_person_by_username(self):
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
                'http://localhost:5000/people/bob',
                data  = {
                    'username': 'bob',
                    'name': 'Jim Billy',
                    'email': 'jbob@example.com',
                    'website': 'http://jbob.example.com',
                })
        
            self.assertEqual(
                json.loads(response.data),
                { 'message': 'person update successful' })

            response = client.get(
                'http://localhost:5000/people/bob')

            self.assertEqual(
                json.loads(response.data),
                {
                    'id': 1,
                    'username': 'bob',
                    'name': 'Jim Billy',
                    'email': 'jbob@example.com',
                    'website': 'http://jbob.example.com',
                })

    def test_update_non_existing_person_by_id(self):
        with self.app.test_client() as client:

            response = client.post(
                'http://localhost:5000/people/1',
                data  = {
                    'username': 'bob',
                    'name': 'Jim Billy',
                    'email': 'jbob@example.com',
                    'website': 'http://jbob.example.com',
                })
        
            self.assertEqual(
                json.loads(response.data),
                { 'message': 'person not found' })


    def test_update_non_existing_person_by_username(self):
        with self.app.test_client() as client:


            response = client.post(
                'http://localhost:5000/people/bob',
                data  = {
                    'username': 'bob',
                    'name': 'Jim Billy',
                    'email': 'jbob@example.com',
                    'website': 'http://jbob.example.com',
                })
        
            self.assertEqual(
                json.loads(response.data),
                { 'message': 'person not found' })

