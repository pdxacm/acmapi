from flask.ext.restful.fields import Integer
from flask.ext.restful.fields import String
from flask.ext.restful.fields import Boolean
from flask.ext.restful.fields import Url
from flask.ext.restful.fields import Raw
from flask.ext.restful.fields import List
from flask.ext.restful.fields import Nested

from .field_types import UrlUsage
from .field_types import UrlWithParams
from .field_types import DateTime
from .field_types import Date

from . import DATE_FORMAT
from . import DATETIME_FORMAT

root_fields = {
    'events_url': UrlUsage('events', absolute=True),
    'people_url': UrlUsage('people', absolute=True),
    'posts_url': UrlUsage('posts', absolute=True),
    'memberships_url': UrlUsage('memberships', absolute=True),
    'officerships_url': UrlUsage('officerships', absolute=True),
}

event_fields = {
    'event_id': Integer(attribute='list'),
    'title': String,
    'description': String, 
    'speaker': String,
    'location': String,
    'editor_id': Integer,
    'editor': Url('people', absolute=True),
    'edited_at': DateTime(DATETIME_FORMAT, attribute='edited_datetime'),
    'start': DateTime(DATETIME_FORMAT),
    'end': DateTime(DATETIME_FORMAT),
    'canceled': Boolean,
    'hidden': Boolean,
    'revision': Integer(attribute='index'),
}

post_fields = {
    'post_id': Integer(attribute='list'),
    'title': String,
    'description': String, 
    'editor_id': Integer,
    'editor': Url('people', absolute=True),
    'edited_at': DateTime(DATETIME_FORMAT, attribute='edited_datetime'),
    'hidden': Boolean,
    'revision': Integer(attribute='index'),
    'content': String,
}

person_fields = {
    'id': Integer,
    'username': String,
    'name': String,
    'email': String,
    'website': String,
    'gravatar_email': String,
    'gravatar_id': String,
    'avatar_url': String,
}

membership_fields = {
    'id': Integer,
    'start_date': Date(DATE_FORMAT),
    'end_date': Date(DATE_FORMAT),
    'person_id': Integer,
    'person': Url('people', absolute=True),
}

officership_fields = {
    'id': Integer,
    'title': String,
    'start_date': Date(DATE_FORMAT),
    'end_date': Date(DATE_FORMAT),
    'person_id': Integer,
    'person': Url('people', absolute=True),
}


database_fields = {
    'dilect': String,
    'host': String,
    'port': Integer,
    'database': String,
    'username': String,
    'password': String,
}
