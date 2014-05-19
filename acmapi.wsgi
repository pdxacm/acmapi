#!/usr/bin/env python

from acmapi import create_app

application = create_app(None, None, 'SQLALCHEMY_DATABASE_URI')
