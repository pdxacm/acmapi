from . import models
from .models import DB

import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound

""" People """

def people(page=None, pagesize=None):
    return models.Person.query\
        .limit(pagesize)\
        .offset((page-1)*pagesize)

def people_count():
    return DB.session.query(
        sqlalchemy.func.count(
            models.Person.id)
        ).one()[0]

def person_id(id):
    return models.Person.query.get(id)

def person_username(username):
    try:
        return models.Person.query\
            .filter_by(username=username).one()
    except NoResultFound:
        return None 

""" Membership """

def membership(id):
    return models.Membership.query.get(id)

def memberships(page, pagesize):
    return list(models.Membership.query\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def memberships_count():
    return DB.session.query(
            sqlalchemy.func.count(models.Membership.id))\
        .one()[0]

""" Officerships """

def officership(id):
    return models.Officership.query.get(id)

def officerships(page, pagesize):
    return list(models.Officership.query\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def officerships_count():
    return DB.session.query(
            sqlalchemy.func.count(models.Officership.id))\
        .one()[0]

""" Posts """

def post(id):
    return models.Post.query.get(id)

def posts_list(list_id, page=None, pagesize=None):
    return list(models.Post.query\
        .filter_by( list=list_id)\
        .order_by(models.Post.index)\
        .limit(pagesize)\
        .offset(page-1))

def posts_list_count(list_id):
    return DB.session.query(
            sqlalchemy.func.count(models.Post.id))\
        .filter_by(list=list_id)\
        .order_by(models.Post.index)\
        .one()[0]

def posts(page, pagesize):
    sub = DB.session.query(
        models.Post.list,
        sqlalchemy.func.max(models.Post.index).label('max_index')
    ).group_by(models.Post.list).subquery()

    return list(DB.session.query(models.Post)\
        .join(sub, models.Post.index==sub.c.max_index)\
        .filter(models.Post.list==sub.c.list)\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def posts_count():
    sub = DB.session.query(
        models.Post.list,
        sqlalchemy.func.max(models.Post.index).label('max_index')
    ).group_by(models.Post.list).subquery()

    return DB.session.query(
            sqlalchemy.func.count(models.Post.id))\
        .join(sub, models.Post.index==sub.c.max_index)\
        .filter(models.Post.list==sub.c.list)\
        .one()[0]

""" Events """

def event(id):
    return models.Event.query.get(id)

def events_list(list_id, page=None, pagesize=None):
    return list(models.Event.query\
        .filter_by(list=list_id)\
        .order_by(models.Event.index)\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def events_list_count(list_id):
    return DB.session.query(
            sqlalchemy.func.count(models.Event.id))\
        .filter_by(list=list_id)\
        .order_by(models.Event.index)\
        .one()[0]

def events(page=None, pagesize=None):
    sub = DB.session.query(
        models.Event.list,
        sqlalchemy.func.max(models.Event.index).label('max_index')
    ).group_by(models.Event.list).subquery()

    return list(DB.session.query(models.Event)\
        .join(sub, models.Event.index==sub.c.max_index)\
        .filter(models.Event.list==sub.c.list)\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def events_count():
    sub = DB.session.query(
        models.Event.list,
        sqlalchemy.func.max(models.Event.index).label('max_index')
    ).group_by(models.Event.list).subquery()

    return DB.session.query(
            sqlalchemy.func.count(models.Event.id))\
        .join(sub, models.Event.index==sub.c.max_index)\
        .filter(models.Event.list==sub.c.list)\
        .one()[0]

""" Officers """

def active_officers(page, pagesize):
    """ returns all of the people who are active officers """

    sub = DB.session.query(
            models.Officership.person_id.label('person_id'))\
        .filter(
            models.Officership.start_date <= sqlalchemy.func.current_date(),
            sqlalchemy.or_(
                models.Officership.end_date >= sqlalchemy.func.current_date(),
                models.Officership.end_date == None))\
        .subquery()

    return list(DB.session.query(
            models.Person)\
        .join(sub, models.Person.id == sub.c.person_id)\
        .distinct()\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def active_officers_count():
    """ returns the number of people who are active officers """
    sub = DB.session.query(
            models.Officership.person_id.label('person_id'))\
        .filter(
            models.Officership.start_date <= sqlalchemy.func.current_date(),
            sqlalchemy.or_(
                models.Officership.end_date >= sqlalchemy.func.current_date(),
                models.Officership.end_date == None))\
        .subquery()

    return DB.session.query(
            sqlalchemy.func.count(models.Person.id))\
        .join(sub, models.Person.id == sub.c.person_id)\
        .distinct().one()[0]

""" Members """

def active_members(page, pagesize):
    """ returns all of the people who are active members """

    sub = DB.session.query(
            models.Membership.person_id.label('person_id'))\
        .filter(
            models.Membership.start_date <= sqlalchemy.func.current_date(),
            sqlalchemy.or_(
                models.Membership.end_date >= sqlalchemy.func.current_date(),
                models.Membership.end_date == None))\
        .subquery()

    return list(DB.session.query(
            models.Person)\
        .join(sub, models.Person.id == sub.c.person_id)\
        .distinct()\
        .limit(pagesize)\
        .offset((page-1)*pagesize))

def active_members_count():
    """ returns the number of people who are active members """
    sub = DB.session.query(
            models.Membership.person_id.label('person_id'))\
        .filter(
            models.Membership.start_date <= sqlalchemy.func.current_date(),
            sqlalchemy.or_(
                models.Membership.end_date >= sqlalchemy.func.current_date(),
                models.Membership.end_date == None))\
        .subquery()

    return DB.session.query(
            sqlalchemy.func.count(models.Person.id))\
        .join(sub, models.Person.id == sub.c.person_id)\
        .distinct().one()[0]
