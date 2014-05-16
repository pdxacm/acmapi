import flask
from flask.ext.httpauth import HTTPBasicAuth
from .models import Person

AUTH = HTTPBasicAuth()

@AUTH.verify_password
def verify_password(username, password):
    person = Person.query.filter_by(username = username).first()
    if not person or not person.verify_password(password):
        return False
    flask.g.person = person
    return True
