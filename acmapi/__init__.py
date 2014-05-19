from flask import Flask
from flask.ext import restful

import os

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = '%Y-%m-%d'

__version__ = '0.1.0'

from .models import DB
from .resources import \
    API, Root, Events, People, Memberships, Officerships
from .authentication import AUTH

def create_app(config_files=None, envvars_files=None, *envvars, **other):
    app = Flask(__name__)
    
    for i in iterable(config_files):
        app.config.from_pyfile(i)

    for i in iterable(envvars_files): 
        app.config.from_envvar(i)
    
    for i in iterable(envvars):
        app.config[i] = os.environ[i]

    for key, value in other.items():
        app.config[key] = value
    
    DB.init_app(app)

    API.init_app(app)

    return app

def iterable(x):
    if x is None:
        return ()
    elif not hasattr(x, '__iter__'):
        return tuple(x)
    else:
        return x
