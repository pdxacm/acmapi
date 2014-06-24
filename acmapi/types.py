"""
acmapi.types

These function are types for reqparse arguments.
"""

import datetime

from . import DATE_FORMAT
from . import DATETIME_FORMAT

class ValidationError(Exception):
    pass

def date_type(x):
    """ A function which acts as a type for reqparse.
    
    Given a string this function will return a date object if the string
    is in the currect format. If the format is incorrect a
    ValidationError is raised.

    >>> date_type('2014-04-11')
    datetime.date(2014, 4, 11)
    """
    try:
        return datetime.datetime.strptime(x, DATE_FORMAT).date()
    except ValueError:
        raise ValidationError(
            'Must be a valid datetime in the {} format'.format(DATETIME_FORMAT))

def datetime_type(x):
    """ A function which acts as a type for reqparse.

    Given a string this function will return a datetime object if the 
    string is in the currect format. If the format is incorrect a
    ValidationError is raised.

    >>> datetime_type('2014-04-11 16:20:00.00000')
    datetime.datetime(2014, 4, 11, 16, 20)
    """
    try:
        return datetime.datetime.strptime(x, DATETIME_FORMAT)
    except ValueError as error:
        raise ValidationError(
            "Must be a valid datetime in the {} format".format(DATETIME_FORMAT))
