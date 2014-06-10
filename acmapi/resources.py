import flask
from flask import Flask, current_app
from flask.ext import restful
from flask.ext.restful import \
    reqparse, fields, marshal_with, marshal, abort

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

import datetime

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse 

from . import models
from .models import DB
from .fields import \
    DateField, MarshallingException, \
    root_fields, event_fields, post_fields, person_fields, \
    membership_fields, officership_fields, database_fields
from .types import \
    datetime_type, date_type
from .authentication import AUTH
from .argument import CustomArgument


API = restful.Api()

def _handle_error(error):
    abort(400, message=str(error), exception=error.__class__.__name__)

def _get_person_by_id(person_id):
    return models.Person.query.get(person_id)

def _get_person_by_username(username):
    try:
        return models.Person.query.filter_by(username=username).one()
    except NoResultFound:
        return None 

def _get_membership_by_id(membership_id):
    return models.Membership.query.get(membership_id)

def _get_officership_by_id(officership_id):
    return models.Officership.query.get(officership_id)

def _get_post_by_list(list_id, page, pagesize):
    return list(models.Post.query.filter_by(
            list=list_id).order_by(
                    models.Post.index).limit(pagesize).offset(page-1))

def _get_event_by_list(list_id, page, pagesize):
    return list(models.Event.query.filter_by(
            list=list_id).order_by(
                    models.Event.index).limit(pagesize).offset(page-1))

class Root(restful.Resource):
    @marshal_with(root_fields)
    def get(self):
        return {}

class Events(restful.Resource):

    def get(self, event_id=None):

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()

        DB.create_all()

        if event_id:

            event = _get_event_by_list(event_id, args.page, args.pagesize)
            if not event:
                _handle_error(LookupError('event not found'))
            
            return marshal(event, event_fields)

        else:
        
                
            sub = DB.session.query(
                models.Event.list,
                sqlalchemy.func.max(models.Event.index).label('max_index')
            ).group_by(models.Event.list).subquery()

            events = DB.session.query(models.Event)\
                    .join(sub, models.Event.index==sub.c.max_index)\
                    .filter(models.Event.list==sub.c.list)\
                    .limit(args.pagesize).offset(args.page-1)
            
            return list(map(
                lambda event: 
                    marshal(event, event_fields), 
                        list(events)))

    @AUTH.login_required
    def post(self):
        """ To add a resource """

        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('hidden', type=bool, default=False)
        parser.add_argument('canceled', type=bool, default=False)
        parser.add_argument('speaker', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('start', type=datetime_type, required=True)
        parser.add_argument('end', type=datetime_type, required=True)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()
        
        list_id, = DB.session.query(
            sqlalchemy.func.max(models.Event.list)).first()
        
        event = models.Event.create(
            title = args.title,
            description = args.description,
            location = args.location,
            speaker = args.speaker,
            hidden = args.hidden,
            canceled = args.canceled,
            start = args.start,
            end = args.end,
            editor = flask.g.person,
            edited_datetime = datetime.datetime.now(),
            index = 1,
            list = list_id+1 if list_id else 1,
        )

        DB.session.add(event)
        DB.session.commit()

        return marshal(event, event_fields) 

    @AUTH.login_required
    def put(self, event_id):
        """ To update a resource """

        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('speaker', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('start', type=datetime_type)
        parser.add_argument('end', type=datetime_type)
        parser.add_argument('hidden', type=bool)
        parser.add_argument('canceled', type=bool)

        args = parser.parse_args()
        
        sub = DB.session.query(
            models.Event.list,
            sqlalchemy.func.max(models.Event.index).label('max_index')
        ).group_by(models.Event.list)\
         .filter(models.Event.list==event_id)\
         .subquery()
        
        try:
            old_event = DB.session.query(models.Event)\
                .join(sub, models.Event.index==sub.c.max_index)\
                .filter(models.Event.list==sub.c.list)\
                .one()
        except NoResultFound:

            _handle_error(LookupError('event not found'))

        else:

            event = models.Event.create(
                title = args.title or old_event.title,
                description = args.description or old_event.description,
                speaker = args.speaker or old_event.speaker,
                location = args.location or old_event.location,
                hidden = args.hidden or old_event.hidden,
                canceled = args.canceled or old_event.canceled,
                start = args.start or old_event.start,
                end = args.end or old_event.end,
                editor = flask.g.person,
                edited_datetime = datetime.datetime.now(),
                index = old_event.index + 1,
                list = old_event.list,
            )
            
            DB.session.commit()

            return marshal(event, event_fields)


class Posts(restful.Resource):

    def get(self, post_id=None):

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()

        DB.create_all()

        if post_id:

            posts = _get_post_by_list(post_id, args.page, args.pagesize)
            if not posts:
                _handle_error(LookupError('post not found'))

            return marshal(posts, post_fields)

        else:

            sub = DB.session.query(
                models.Post.list,
                sqlalchemy.func.max(models.Post.index).label('max_index')
            ).group_by(models.Post.list).subquery()

        
            posts = DB.session.query(models.Post)\
                .join(sub, models.Post.index==sub.c.max_index)\
                .filter(models.Post.list==sub.c.list)\
                .limit(args.pagesize).offset(args.page-1)

            return list(map(
                lambda post: 
                    marshal(post, post_fields), 
                    list(posts)))
        
    @AUTH.login_required
    def post(self):

        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('hidden', type=bool, default=False)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()
        
        list_id, = DB.session.query(
            sqlalchemy.func.max(models.Post.list)).first()

        post = models.Post.create(
            title = args.title,
            description = args.description,
            content = args.content,
            hidden = args.hidden,
            editor = flask.g.person,
            edited_datetime = datetime.datetime.now(),
            index = 1,
            list = list_id+1 if list_id else 1,
        )

        DB.session.add(post)
        DB.session.commit()

        return marshal(post, post_fields) 

    @AUTH.login_required
    def put(self, post_id):
        """ To update a resource """

        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('hidden', type=bool)

        args = parser.parse_args()
        
        sub = DB.session.query(
            models.Post.list,
            sqlalchemy.func.max(models.Post.index).label('max_index')
        ).group_by(models.Post.list)\
         .filter(models.Post.list==post_id)\
         .subquery()
        
        try:
            old_post = DB.session.query(models.Post)\
                    .join(sub, models.Post.index==sub.c.max_index)\
                    .filter(models.Post.list==sub.c.list)\
                    .one()

        except NoResultFound:
            _handle_error(LookupError('post not found'))

        else:

            post = models.Post.create(
                title = args.title or old_post.title,
                description = args.description or old_post.description,
                content = args.content or old_post.content,
                hidden = args.hidden or old_post.hidden,
                editor = flask.g.person,
                edited_datetime = datetime.datetime.now(),
                index = old_post.index + 1,
                list = old_post.list,
            )
            
            DB.session.commit()

            return marshal(post, post_fields)


class People(restful.Resource):
    
    def get(self, person_id=None, username=None):
        
        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()

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
                _handle_error(LookupError('person not found'))
        
        else:

            people = models.Person.query.limit(args.pagesize).offset(args.page-1)

            return list(map(
                lambda person: 
                    marshal(person, person_fields), 
                list(people)))

    @AUTH.login_required
    def post(self):
        
        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('username', type=str, required=True)
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('website', type=str)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('gravatar_email', type=str)

        args = parser.parse_args()

        person = models.Person.create(
            username = args.username,
            name = args.name,
            email = args.email,
            website = args.website,
            password = args.password,
            gravatar_email = args.gravatar_email)
        
        DB.session.add(person)

        try: 
            DB.session.commit()
        except IntegrityError:
            return { 'message': 'username already exists' }

        return marshal(person, person_fields)

    @AUTH.login_required
    def put(self, person_id=None, username=None):

        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        if person_id or username:

            parser.add_argument('username', type=str)
            parser.add_argument('name', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('website', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('gravatar_email', type=str)

            args = parser.parse_args()

            if person_id:
                person = _get_person_by_id(person_id)

            elif username:
                person = _get_person_by_username(username) 

            else:
                person = None

            if not person:
                _handle_error(LookupError('person not found'))
        
            
            if args.username:
                person.username = args.username
            if args.name:
                person.name = args.name
            if args.email:
                person.email = args.email
            if args.website:
                person.website = args.website
            if args.password:
                person.password_hash = person.hash_password(args.password)
            if args.gravatar_email:
                person.set_gravatar_email(args.gravatar_email)
            
            try:
                DB.session.commit()
            except IntegrityError:
                return _handle_error(ValueError('username already exists'))

            return marshal(person, person_fields)

        else:

            flask.abort(404)

    @AUTH.login_required
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
                _handle_error(LookupError('person not found'))
        
        else:

            # XXX This should never happen
            return {'message': 'delete failed, nothing to delete'}

class Memberships(restful.Resource):

    def get(self, membership_id=None):

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()

        DB.create_all()

        if membership_id:

            membership = _get_membership_by_id(membership_id)

            if membership:
                return marshal(membership, membership_fields)
            else:
                _handle_error(LookupError('membership not found'))

        else:

            return list(map(
                lambda membership: 
                    marshal(membership, membership_fields), 
                list(models.Membership.query.limit(args.pagesize).offset(args.page-1))))

    @AUTH.login_required
    def post(self):
       
        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('person_id', type=int, required=True)
        parser.add_argument('start_date', type=date_type, required=True)
        parser.add_argument('end_date', type=date_type)
        
        args = parser.parse_args()

        person = _get_person_by_id(args.person_id)
        if not person:
            _handle_error(LookupError('person not found'))

        membership = models.Membership.create(
            person = person,
            start_date = args.start_date,
            end_date = args.end_date)

        DB.session.add(membership)

        try:
            DB.session.commit()
        except IntegrityError:
            _handle_error(ValueError('start_date must be less than end_date'))
        
        return marshal(membership, membership_fields)

    @AUTH.login_required
    def put(self, membership_id):
       
        DB.create_all()

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('person_id', type=int)
        parser.add_argument('start_date', type=date_type)
        parser.add_argument('end_date', type=date_type)

        args = parser.parse_args()

        membership = _get_membership_by_id(membership_id)
        if not membership:
            _handle_error(LookupError('membership not found'))
        
        if args.person_id:
            person = _get_person_by_id(args.person_id)
            if not person:
                return _handle_error(ValueError('not a valid person_id'))
            membership.person_id = args.person_id

        if args.start_date:
            membership.start_date = args.start_date

        if args.end_date:
            membership.end_date = args.end_date
        
        try:
            DB.session.commit()
        except IntegrityError:
            _handle_error(ValueError('start_date must be less than end_date'))

        return marshal(membership, membership_fields)
    
    @AUTH.login_required
    def delete(self, membership_id):

        DB.create_all()

        membership = _get_membership_by_id(membership_id)
        if not membership:
            _handle_error(LookupError('membership not found'))


        DB.session.delete(membership)
        DB.session.commit()

        return {'message': 'delete successful'}

class Officerships(restful.Resource):

    parser = reqparse.RequestParser(argument_class=CustomArgument)
    parser.add_argument('person_id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('start_date', type=str)
    parser.add_argument('end_date', type=str)

    def get(self, officership_id=None):

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)
        
        args = parser.parse_args()

        DB.create_all()
        
        if officership_id:

            officership = _get_officership_by_id(officership_id)

            if officership:
                return marshal(officership, officership_fields)
            else:
                _handle_error(LookupError('officership not found'))

        else:

            return list(map(
                lambda officership: 
                    marshal(officership, officership_fields), 
                list(models.Officership.query.limit(args.pagesize).offset(args.page-1))))

    @AUTH.login_required
    def post(self):

        DB.create_all()
        
        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('person_id', type=int, required=True)
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('start_date', type=date_type, required=True)
        parser.add_argument('end_date', type=date_type)
        
        args = parser.parse_args()

        person = _get_person_by_id(args.person_id)
        if not person:
            _handle_error(LookupError('person not found'))

        officership = models.Officership.create(
            person = person,
            title = args.title,
            start_date = args.start_date,
            end_date = args.end_date)

        DB.session.add(officership)

        try:
            DB.session.commit()
        except IntegrityError:
            _handle_error(ValueError('start_date must be less than end_date'))

        return marshal(officership, officership_fields)

    @AUTH.login_required
    def put(self, officership_id):

        DB.create_all()
        
        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('person_id', type=int)
        parser.add_argument('title', type=str)
        parser.add_argument('start_date', type=date_type)
        parser.add_argument('end_date', type=date_type)

        args = parser.parse_args()

        officership = _get_officership_by_id(officership_id)
        if not officership:
            _handle_error(LookupError('officership not found'))
        
        if args.person_id:
            person = _get_person_by_id(args.person_id)
            if not person:
                _handle_error(LookupError('person not found'))
            officership.person_id = args.person_id

        if args.start_date:
            officership.start_date = args.start_date

        if args.end_date:
            officership.end_date = args.end_date
    
        try:
            DB.session.commit()
        except IntegrityError:
            _handle_error(ValueError('start_date must be less than end_date'))

        return marshal(officership, officership_fields)

    @AUTH.login_required
    def delete(self, officership_id):

        DB.create_all()

        officership = _get_officership_by_id(officership_id)
        if not officership:
            _handle_error(LookupError('officership not found'))

        DB.session.delete(officership)
        DB.session.commit()

        return {'message': 'delete successful'}

class Database(restful.Resource):

    @AUTH.login_required
    def get(self):

        parser = reqparse.RequestParser(argument_class=CustomArgument)

        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int)

        args = parser.parse_args()

        parsed_url = urlparse(current_app.config['SQLALCHEMY_DATABASE_URI'])
        
        username, password, host, port = None, None, None, None

        split_netloc = parsed_url.netloc.split('@')
        if len(split_netloc) == 2:
            host = split_netloc[1]
            username_password = split_netloc[0].split(':')
            if len(username_password) == 2:
                username = username_password[0]
                password = username_password[1]
            else:
                username = username_password[0]
        elif len(split_netloc) == 1:
            host = split_netloc[0]
        
        split_host = host.split(':')
        if len(split_host) == 2:
            host = split_host[0]
            port = split_host[1]
        elif len(split_host) == 1:
            host = split_host[0]

        database = {
            'dilect': parsed_url.scheme,
            'host': host,
            'port': port,
            'database': parsed_url.path.strip('/'),
            'username': username,
            'password': password}

        return marshal(database, database_fields)

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

API.add_resource(
    Database, 
    '/database/',
    endpoint='database')
