from flask.ext.sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Event(DB.Model):
   
    __tablename__ = "events"

    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.Unicode)
    description = DB.Column(DB.UnicodeText)
    speaker = DB.Column(DB.Unicode)
    location = DB.Column(DB.Unicode)
    editor_id = DB.Column(DB.Integer, DB.ForeignKey('people.id'), nullable=False)
    edited_datetime = DB.Column(DB.DateTime, nullable=False)
    start = DB.Column(DB.DateTime, nullable=False)
    end = DB.Column(DB.DateTime, nullable=False)
    canceled = DB.Column(DB.Boolean, nullable=False)
    hidden = DB.Column(DB.Boolean, nullable=False)
    list = DB.Column(DB.Integer, nullable=False)
    index = DB.Column(DB.Integer, nullable=False)
    
    __table_args__ = (
        DB.UniqueConstraint(list, index),
        DB.CheckConstraint(start < end),
    )

    def __repr__(self):
        return "<Event({})>".format(self.id)

    @classmethod
    def create(cls, title, description, speaker, location, 
            start, end, editor, edited_datetime, list, index,
            canceled=False, hidden=False):

        x = cls()
        x.title = title
        x.description = description
        x.speaker = speaker
        x.location = location
        x.editor = editor
        x.edited_datetime = edited_datetime
        x.start = start
        x.end = end
        x.canceled = canceled
        x.hidden = hidden
        x.list = list
        x.index = index
        return x

class Post(DB.Model):

    __tablename__ = "posts"

    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.Unicode)
    description = DB.Column(DB.UnicodeText)
    content = DB.Column(DB.UnicodeText)
    editor_id = DB.Column(DB.Integer, DB.ForeignKey('people.id'), nullable=None)
    edited_datetime = DB.Column(DB.DateTime, nullable=None)
    hidden = DB.Column(DB.Boolean, nullable=None)
    list = DB.Column(DB.Integer, nullable=False)
    index = DB.Column(DB.Integer, nullable=False)
    
    __table_args__ = (
        DB.UniqueConstraint(list, index),
    )

    @classmethod
    def create(cls, title, description, content, editor, edited_datetime, 
            hidden, list, index):
        
        x = cls()
        x.title = title
        x.description = description
        x.content = content
        x.editor = editor
        x.edited_datetime = edited_datetime
        x.hidden = hidden
        x.list = list
        x.index = index
        return x

    def __repr__(self):
        return "<Post({})>".format(self.id)


class Person(DB.Model):

    __tablename__ = "people"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode)
    username = DB.Column(DB.Unicode, unique=True, nullable=False)
    email = DB.Column(DB.Unicode)
    website = DB.Column(DB.Unicode)

    memberships = DB.relationship(
        'Membership', 
        backref='person', 
        lazy='dynamic',
    )

    officerships = DB.relationship(
        'Officership', 
        backref='person', 
        lazy='dynamic',
    )

    events_edited = DB.relationship(
        'Event', 
        backref='editor', 
        lazy='dynamic',
    )

    posts_edited = DB.relationship(
        'Post', 
        backref='editor', 
        lazy='dynamic',
    )
    
    @classmethod
    def create(cls, name, username, email, website):

        x = cls()
        x.name = name
        x.username = username
        x.email = email
        x.website = website
        return x

    def __repr__(self):
        return "<Person({})>".format(self.id)


class Officership(DB.Model):
    
    __tablename__ = "officerships"

    id = DB.Column(DB.Integer, primary_key=True)
    person_id = DB.Column(DB.Integer, DB.ForeignKey('people.id'), nullable=False)
    title = DB.Column(DB.Unicode, nullable=False)
    start_date = DB.Column(DB.Date, nullable=False)
    end_date = DB.Column(DB.Date)

    __table_args__ = (
        DB.CheckConstraint(end_date is None or start_date < end_date),
    )

    @classmethod
    def create(cls, person, title, start_date, end_date):

        x = cls()
        x.person = person
        x.title = title
        x.start_date = start_date
        x.end_date = end_date
        return x

    def __repr__(self):
        return "<Officership({})>".format(self.id)


class Membership(DB.Model):

    __tablename__ = "memberships"

    id = DB.Column(DB.Integer, primary_key=True)
    person_id = DB.Column(DB.Integer, DB.ForeignKey('people.id'), nullable=False)
    start_date = DB.Column(DB.Date, nullable=False)
    end_date = DB.Column(DB.Date)
    
    __table_args__ = (
        DB.CheckConstraint(end_date is None or start_date < end_date),
    )

    @classmethod
    def create(cls, person, start_date, end_date=None):

        x = cls()
        x.person = person
        x.start_date = start_date
        x.end_date = end_date
        return x

    def __repr__(self):
        return "<Membership({})>".format(self.id)
