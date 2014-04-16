from flask.ext.restful.fields import \
    Integer, String, DateTime, Boolean, Url, Raw

from . import DATE_FORMAT, DATETIME_FORMAT

class MarshallingException(Exception):
    pass

class DateField(Raw):
    def format(self, x):
        try:
            return x.strftime(DATE_FORMAT)
        except AttributeError:
            raise MarshallingException("Must be a valid date")

root_fields = {
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
