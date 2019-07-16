#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" record.py biflorica's marketplace spider """

__author__ = 'Néstor Bohórquez'
__copyright__ = 'Copyright 2015'
__credits__ = []
__license__ = 'Apache License Version 2.0'
__version__ = '0.0.1'
__maintainer__ = 'Néstor Bohórquez'
__email__ = 'tca7410nb@gmail.com'
__status__ = 'Hack'

import sys

from biflorica.api import APISession, MarketPlace
from biflorica.orm import (
  initialize as initialize_db, Session as DBSession, Trade
)

def main():
  initialize_db()

  # Fool the russians!!
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0'
  }
  api = APISession(headers)
  db = DBSession()

  start = 1
  limit = 26
  terminate = False

  api.users.login.post()
  # This loop will keep rolling until we process all trades ahead of the latest
  # one we have stored in the database
  while(not terminate):
    r = api.marketplace.get(start=start, limit=limit)
    for t in r.trades:
      try:
        db.add(Trade(**t.__dict__))
        db.commit()
      except:
        # We get here when we try to process a repeated row.
        db.rollback()
        print "[ERROR]: {0} - {1}".format(sys.exc_info()[0], sys.exc_info()[1])
        terminate = True
        break
    start += limit
  api.users.logout.get()
  db.close()

if __name__ == '__main__':
  main()
