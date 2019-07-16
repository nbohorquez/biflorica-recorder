#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser, datetime, locale, time

from datetime import date

locale.setlocale(locale.LC_ALL, '')

CONFIG_FILE = 'config.ini'
config = ConfigParser.ConfigParser()
with open(CONFIG_FILE) as fp:
  config.readfp(fp)

class UnrecognizedDateFormatError(Exception):
  def __init__(self, message, date):
    super(UnrecognizedDateFormatError, self).__init__(message)
    self.date = date

def parse_date(date=None):
  try:
    time_st = time.strptime(date, '%d de %B de %Y')
    return datetime.date.fromtimestamp(time.mktime(time_st))
  except ValueError:
    pass

  try:
    time_st = time.strptime(date, '%d de %B')
    return datetime.date.fromtimestamp(time.mktime(time_st))
  except ValueError:
    pass

  try:
    time_st = time.strptime(date, '%Y')
    return datetime.date.fromtimestamp(time.mktime(time_st))
  except ValueError:
    pass

  raise UnrecognizedDateFormatError("Could not parse date", date)
