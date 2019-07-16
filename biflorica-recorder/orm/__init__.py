#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.engine import Engine
from sqlalchemy.event import listens_for
from sqlalchemy.orm import sessionmaker

from schema import Base, Color, Type, Variety, Size, Farm, Trade

Session = sessionmaker()

def db_params(**kwargs):
  from biflorica.commons import config

  try:
    return kwargs['sqlalchemy.url'], True
  except KeyError:
    pass

  try:
    return config.get('db', 'url'), {'yes': True, 'no': False}[config.get('db', 'echo')]
  except:
    return '', False

def initialize(**kwargs):
  from sqlalchemy import create_engine

  global Session

  url, echo = db_params(**kwargs)
  try:
    engine = create_engine(url, echo=echo)
  except:
    raise Exception('Impossible to create the database engine')

  Base.metadata.create_all(engine)
  Session.configure(bind=engine)
