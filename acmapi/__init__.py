from flask import Flask

from .database import DB

__version__ = '0.1.0'

def create_app(config_files=None, envvars=None, **other):
    app = Flask(__name__)
    
    for i in iterable(config_files):
        app.config.from_pyfile(i)

    for i in iterable(envvars): 
        app.config.from_envvar(i)

    for key, value in other.items():
        app.config[key] = value
    
    DB.init_app(app)
    
    return app

def iterable(x):
    if x is None:
        return ()
    elif not hasattr(x, '__iter__'):
        return tuple(x)
    else:
        return x
