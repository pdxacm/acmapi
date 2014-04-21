import flask
from flask import Flask
from flask.ext import restful
from flask.ext.restful import \
    reqparse, fields, marshal_with, marshal

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

import datetime

from . import database
from .database import DB
from .fields import \
    DateField, MarshallingException, \
    root_fields, event_fields, post_fields, person_fields, \
    membership_fields, officership_fields
from .types import \
    datetime_type, date_type


API = restful.Api()

def _get_person_by_id(person_id):
    return database.Person.query.get(person_id)

def _get_person_by_username(username):
    try:
        return database.Person.query.filter_by(username=username).one()
    except NoResultFound:
        return None 

def _get_membership_by_id(membership_id):
    return database.Membership.query.get(membership_id)

def _get_officership_by_id(officership_id):
    return database.Officership.query.get(officership_id)

def _get_post_by_list(list_id):
    return database.Post.query.filter_by(
            list=list_id).order_by(
                    database.Post.index).all()

def _get_event_by_list(list_id):
    return database.Event.query.filter_by(
            list=list_id).order_by(
                    database.Event.index).all()

class Root(restful.Resource):
    @marshal_with(root_fields)
    def get(self):
        return {}

class Events(restful.Resource):

    def get(self, event_id=None):

        DB.create_all()

        if event_id:

            event = _get_event_by_list(event_id)

            return marshal(event, event_fields)

        else:

            events = DB.session.query(
                database.Event,
                sqlalchemy.func.max(database.Event.index)
            ).group_by(database.Event.list).all()
            
            return list(map(
                lambda event: 
                    marshal(event[0], event_fields), 
                    events))

    def post(self, event_id=None):

        DB.create_all()

        parser = reqparse.RequestParser()

        if event_id:

            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('speaker', type=str)
            parser.add_argument('location', type=str)
            parser.add_argument('start', type=datetime_type)
            parser.add_argument('end', type=datetime_type)
            parser.add_argument('hidden', type=bool)
            parser.add_argument('canceled', type=bool)

            args = parser.parse_args()
            
            old_event = DB.session.query(
                database.Event,
                sqlalchemy.func.max(database.Event.index)
            ).filter_by(list = event_id).order_by(database.Event.index).one()[0]

            event = database.Event.create(
                title = args.title if args.title else old_event.title,
                description = args.description if args.description else old_event.description,
                speaker = args.speaker if args.speaker else old_event.speaker,
                location = args.location if args.location else old_event.location,
                hidden = args.hidden if args.hidden else old_event.hidden,
                canceled = args.canceled if args.canceled else old_event.canceled,
                start = args.start if args.start else old_event.start,
                end = args.end if args.end else old_event.end,
                editor = _get_person_by_id(1),
                edited_datetime = datetime.datetime.now(),
                index = old_event.index + 1,
                list = old_event.list,
            )
            
            DB.session.commit()

            return marshal(event, event_fields)

        else:

            parser.add_argument('title', type=str, required=True)
            parser.add_argument('description', type=str, required=True)
            parser.add_argument('location', type=str, required=True)
            parser.add_argument('hidden', type=bool, default=False)
            parser.add_argument('canceled', type=bool, default=False)
            parser.add_argument('speaker', type=str, required=True)
            parser.add_argument('location', type=str, required=True)
            parser.add_argument('start', type=datetime_type, required=True)
            parser.add_argument('end', type=datetime_type, required=True)

            args = parser.parse_args()
            
            list_id, = DB.session.query(
                sqlalchemy.func.max(database.Event.list)).first()

            event = database.Event.create(
                title = args.title,
                description = args.description,
                location = args.location,
                speaker = args.speaker,
                hidden = args.hidden,
                canceled = args.canceled,
                start = args.start,
                end = args.end,
                editor = _get_person_by_id(1),
                edited_datetime = datetime.datetime.now(),
                index = 1,
                list = list_id+1 if list_id else 1,
            )

            DB.session.add(event)
            DB.session.commit()

            return marshal(event, event_fields) 


class Posts(restful.Resource):

    def get(self, post_id=None):

        DB.create_all()

        if post_id:

            posts = _get_post_by_list(post_id)

            return marshal(posts, post_fields)

        else:

            posts = DB.session.query(
                database.Post,
                sqlalchemy.func.max(database.Post.index)
            ).group_by(database.Post.list).all()
            
            return list(map(
                lambda post: 
                    marshal(post[0], post_fields), 
                    posts))
        
    def post(self, post_id=None):

        DB.create_all()

        parser = reqparse.RequestParser()

        if post_id:

            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('content', type=str)
            parser.add_argument('hidden', type=bool)

            args = parser.parse_args()
            
            old_post = DB.session.query(
                database.Post,
                sqlalchemy.func.max(database.Post.index)
            ).filter_by(list = post_id).order_by(database.Post.index).one()[0]

            post = database.Post.create(
                title = args.title if args.title else old_post.title,
                description = args.description if args.description else old_post.description,
                content = args.content if args.content else old_post.content,
                hidden = args.hidden if args.hidden else old_post.hidden,
                editor = _get_person_by_id(1),
                edited_datetime = datetime.datetime.now(),
                index = old_post.index + 1,
                list = old_post.list,
            )
            
            DB.session.commit()

            return marshal(post, post_fields)

        else:

            parser.add_argument('title', type=str, required=True)
            parser.add_argument('description', type=str, required=True)
            parser.add_argument('content', type=str, required=True)
            parser.add_argument('hidden', type=bool, default=False)

            args = parser.parse_args()
            
            list_id, = DB.session.query(
                sqlalchemy.func.max(database.Post.list)).first()

            post = database.Post.create(
                title = args.title,
                description = args.description,
                content = args.content,
                hidden = args.hidden,
                editor = _get_person_by_id(1),
                edited_datetime = datetime.datetime.now(),
                index = 1,
                list = list_id+1 if list_id else 1,
            )

            DB.session.add(post)
            DB.session.commit()

            return marshal(post, post_fields) 

class People(restful.Resource):
    
    def get(self, person_id=None, username=None):
        
        DB.create_all()
        
        if person_id or username:
            
            if person_id:
                person = _get_person_by_id(person_id)

            elif username:
                person = _get_person_by_username(username) 

            else:
                person = None
            
            if person:
                return marshal(person, person_fields)
            else:
                return {'message': 'person not found'}
        
        else:

            people = database.Person.query.all()

            return list(map(
                lambda person: 
                    marshal(person, person_fields), 
                people))

    def post(self, person_id=None, username=None):
        
        DB.create_all()

        parser = reqparse.RequestParser()

        if person_id or username:

            parser.add_argument('username', type=str)
            parser.add_argument('name', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('website', type=str)

            args = parser.parse_args()

            if person_id:
                person = _get_person_by_id(person_id)

            elif username:
                person = _get_person_by_username(username) 

            else:
                person = None

            if not person:
                return {'message': 'person not found'}
            
            if args.username:
                person.username = args.username
            if args.name:
                person.name = args.name
            if args.email:
                person.email = args.email
            if args.website:
                person.website = args.website
            
            try:
                DB.session.commit()
            except IntegrityError:
                return { 'message': 'username already exists' }

            return { 'message': 'person update successful' }
        
        else:

            parser.add_argument('username', type=str, required=True)
            parser.add_argument('name', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('website', type=str)

            args = parser.parse_args()

            person = database.Person.create(
                username = args.username,
                name = args.name,
                email = args.email,
                website = args.website)
            
            DB.session.add(person)

            try: 
                DB.session.commit()
            except IntegrityError:
                return { 'message': 'username already exists' }

            return marshal(person, person_fields)

    def delete(self, person_id=None, username=None):

        DB.create_all()

        if person_id or username:
            
            if person_id:
                person = _get_person_by_id(person_id)

            elif username:
                person = _get_person_by_username(username) 

            else:
                person = None
            
            if person:
                DB.session.delete(person)
                DB.session.commit()
                return {'message': 'delete successful'}
            else:
                return {'message': 'delete failed, person not found'}
        
        else:

            # XXX This should never happen
            return {'message': 'delete failed, nothing to delete'}

class Memberships(restful.Resource):

    def get(self, membership_id=None):
        
        DB.create_all()

        if membership_id:

            membership = _get_membership_by_id(membership_id)

            if membership:
                return marshal(membership, membership_fields)
            else:
                return {'message': 'membership not found'}

        else:

            return list(map(
                lambda membership: 
                    marshal(membership, membership_fields), 
                database.Membership.query.all()))

    def post(self, membership_id=None):
       
        DB.create_all()

        parser = reqparse.RequestParser()

        if membership_id:

            parser.add_argument('person_id', type=int)
            parser.add_argument('start_date', type=date_type)
            parser.add_argument('end_date', type=date_type)

            args = parser.parse_args()

            membership = _get_membership_by_id(membership_id)
            if not membership:
                return {'message': 'membership not found'}
            
            if args.person_id:
                person = _get_person_by_id(args.person_id)
                if not person:
                    return {'message': 'not a valid person_id'}
                membership.person_id = args.person_id

            if args.start_date:
                membership.start_date = args.start_date

            if args.end_date:
                membership.end_date = args.end_date
            
            try:
                DB.session.commit()
            except IntegrityError:
                return {'message': 'start_date must be less than end_date'}

            return {'message': 'membership update successful'}

        else:

            parser.add_argument('person_id', type=int, required=True)
            parser.add_argument('start_date', type=date_type, required=True)
            parser.add_argument('end_date', type=date_type, required=True)
            
            args = parser.parse_args()

            person = _get_person_by_id(args.person_id)
            if not person:
                return {'message': 'not a valid person_id'}

            membership = database.Membership.create(
                person = person,
                start_date = args.start_date,
                end_date = args.end_date)

            DB.session.add(membership)

            try:
                DB.session.commit()
            except IntegrityError:
                return {'message': 'start_date must be less than end_date'}
            
            return marshal(membership, membership_fields)
    
    def delete(self, membership_id):

        DB.create_all()

        membership = _get_membership_by_id(membership_id)
        if not membership:
            return {'message': 'delete failed, membership not found'}

        DB.session.delete(membership)
        DB.session.commit()

        return {'message': 'delete successful'}

class Officerships(restful.Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('person_id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('start_date', type=str)
    parser.add_argument('end_date', type=str)

    def get(self, officership_id=None):

        DB.create_all()
        
        if officership_id:

            officership = _get_officership_by_id(officership_id)

            if officership:
                return marshal(officership, officership_fields)
            else:
                return {'message': 'officership not found'}

        else:

            return list(map(
                lambda officership: 
                    marshal(officership, officership_fields), 
                database.Officership.query.all()))

    def post(self, officership_id=None):

        DB.create_all()
        
        parser = reqparse.RequestParser()

        if officership_id:

            parser.add_argument('person_id', type=int)
            parser.add_argument('title', type=str)
            parser.add_argument('start_date', type=date_type)
            parser.add_argument('end_date', type=date_type)

            args = parser.parse_args()

            officership = _get_officership_by_id(officership_id)
            if not officership:
                return {'message': 'officership not found'}
            
            if args.person_id:
                person = _get_person_by_id(args.person_id)
                if not person:
                    return {'message': 'not a valid person_id'}
                officership.person_id = args.person_id

            if args.start_date:
                officership.start_date = args.start_date

            if args.end_date:
                officership.end_date = args.end_date
        
            try:
                DB.session.commit()
            except IntegrityError:
                return {'message': 'start_date must be less than end_date'}

            return {'message': 'officership update successful'}

        else:

            parser.add_argument('person_id', type=int, required=True)
            parser.add_argument('title', type=str, required=True)
            parser.add_argument('start_date', type=date_type, required=True)
            parser.add_argument('end_date', type=date_type, required=True)
            
            args = parser.parse_args()

            person = _get_person_by_id(args.person_id)
            if not person:
                return {'message': 'not a valid person_id'}

            officership = database.Officership.create(
                person = person,
                title = args.title,
                start_date = args.start_date,
                end_date = args.end_date)

            DB.session.add(officership)

            try:
                DB.session.commit()
            except IntegrityError:
                return {'message': 'start_date must be less than end_date'}

            return marshal(officership, officership_fields)

    def delete(self, officership_id):

        DB.create_all()

        officership = _get_officership_by_id(officership_id)
        if not officership:
            return {'message': 'delete failed, officership not found'}

        DB.session.delete(officership)
        DB.session.commit()

        return {'message': 'delete successful'}

API.add_resource(
    Root, 
    '/', 
    endpoint='root')

API.add_resource(
    Events, 
    '/events/', 
    '/events/<int:event_id>', 
    endpoint='events')

API.add_resource(
    People, 
    '/people/',
    '/people/<int:person_id>',
    '/people/<int:editor_id>',
    '/people/<string:username>',
    endpoint='people')

API.add_resource(
    Posts, 
    '/posts/',
    '/posts/<int:post_id>',
    endpoint='posts')

API.add_resource(
    Memberships, 
    '/memberships/',
    '/memberships/<int:membership_id>',
    endpoint='memberships')

API.add_resource(
    Officerships, 
    '/officerships/',
    '/officerships/<int:officership_id>',
    endpoint='officerships')

