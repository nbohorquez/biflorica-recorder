#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" setup.py biflorica's database setup """

__author__ = 'Néstor Bohórquez'
__copyright__ = 'Copyright 2015'
__credits__ = []
__license__ = 'Apache License Version 2.0'
__version__ = '0.0.1'
__maintainer__ = 'Néstor Bohórquez'
__email__ = 'tca7410nb@gmail.com'
__status__ = 'Hack'

import sys

from biflorica.api import APISession, Handbook
from biflorica.orm import (
  initialize as initialize_db, Color, Type, Variety, Farm, Size, 
  Session as DBSession
)
from .commons import add_objects

def main():
  # Fool the russians!!
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'
  }
  api = APISession(headers)
  api.users.login.post()
  r = api.handbook.get(sections=[
    api.handbook.PARAMS.sections.FARM(),
    api.handbook.PARAMS.sections.TRADEMARK(),
    api.handbook.PARAMS.sections.TYPE(),
    api.handbook.PARAMS.sections.VARIETY(),
    api.handbook.PARAMS.sections.SIZE(),
  ])
  api.users.logout.get()

  initialize_db()
  db = DBSession()
  add_objects(db, [Farm(**f.__dict__) for f in r.farms])
  add_objects(db, [Type(**t.__dict__) for t in r.types])
  add_objects(db, [Variety(**v.__dict__) for v in r.varieties])
  add_objects(db, [Size(**s.__dict__) for s in r.sizes])
  add_objects(db, [Color('green'), Color('blue')])
  db.close()

if __name__ == '__main__':
  main()
