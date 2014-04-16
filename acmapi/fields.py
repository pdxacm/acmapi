import flask
from flask.ext.restful import fields
from flask.ext.restful.fields import \
    Integer, String, DateTime, Boolean, Url, Raw

from . import DATE_FORMAT, DATETIME_FORMAT

try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

class MarshallingException(Exception):
    pass

class DateField(Raw):
    def format(self, x):
        try:
            return x.strftime(DATE_FORMAT)
        except AttributeError:
            raise MarshallingException("Must be a valid date")

class UrlUsage(Raw):
    
    def __init__(self, endpoint, absolute=False, scheme=None):
        self.endpoint = endpoint
        self.absolute = absolute
        self.scheme = scheme

    def output(self, obj, key):
        urls = []
        for rule in flask.current_app.url_map.iter_rules():
            if rule.endpoint == self.endpoint:
                o = urlparse(flask.url_for(self.endpoint, _external = self.absolute))
                scheme = self.scheme if self.scheme is not None else o.scheme
                urls.append(urlunparse((scheme, o.netloc, rule.rule, "", "", "")))
        return urls

root_fields = {
    'events_url': UrlUsage('events', absolute=True),
    'people_url': UrlUsage('people', absolute=True),
    'posts_url': UrlUsage('posts', absolute=True),
    'memberships_url': UrlUsage('memberships', absolute=True),
    'officerships_url': UrlUsage('officerships', absolute=True),
}

event_fields = {
    'id': Integer,
    'title': String,
    'description': String, 
    'speaker': String,
    'location': String,
    'editor_id': Integer,
    'editor': Url('people', absolute=True),
    'edited_at': DateTime(attribute='edited_datetime'),
    'start': DateTime,
    'end': DateTime,
    'canceled': Boolean,
    'hidden': Boolean,
    'revision': Integer(attribute='index'),
}

post_fields = {
    'id': Integer,
    'title': String,
    'description': String, 
    'editor_id': Integer,
    'editor': Url('people', absolute=True),
    'edited_at': DateTime(attribute='edited_datetime'),
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
}

membership_fields = {
    'id': Integer,
    'start_date': DateField,
    'end_date': DateField,
    'person_id': Integer,
    'person': Url('people', absolute=True),
}

officership_fields = {
    'id': Integer,
    'title': String,
    'start_date': DateField,
    'end_date': DateField,
    'person_id': Integer,
    'person': Url('people', absolute=True),
}
