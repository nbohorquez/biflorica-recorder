#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def add_objects(db, objs):
  try:
    db.add_all(objs)
    db.commit()
  except:
    db.rollback()
    print "[ERROR]: Unsuccessful object addition: {0} - {1}"\
      .format(sys.exc_info()[0], sys.exc_info()[1])

def add_object(db, obj):
  try:
    db.add(obj)
    db.commit()
  except:
    db.rollback()
    print "[ERROR]: Unsuccessful object addition: {0} - {1}"\
      .format(sys.exc_info()[0], sys.exc_info()[1])
