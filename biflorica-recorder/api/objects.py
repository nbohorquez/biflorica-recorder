#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, re, pytz

from decimal import Decimal, InvalidOperation

ec_tz = pytz.timezone('America/Guayaquil')
utc = pytz.utc

class MarketPlace(object):
  def __init__(self, count, list):
    self.trades = []
    if count > 0:
      self.trades = [self.Trade(**t) for t in list]

  class Trade(object):
    re_creation_datetime = r'^(0[1-9]|[1-9]|[12]\d|3[01]) (2[0-3]|1[0-9]|0[0-9]|[^0-9][0-9]):([0-5][0-9]|[0-9])$'
    re_delivery_date = r'(0[1-9]|[1-9]|[12]\d|3[01]) (\w+)$'
    re_expiration_time = r'^(2[0-3]|1[0-9]|0[0-9]|[^0-9][0-9]):([0-5][0-9]|[0-9])$'

    def __init__(self, guid, canBeChosen, adate, exp, farm, hb, id, utime, type,
                 is_standing, variety, price40, price50, price60, price70, price80,
                 price90, price100, price100p, buttons, color, hash):
      self.id = id
      self.guid = guid
      self.hash = hash
      self.color = color
      self.type_id = type
      self.variety_id = variety
      self.farm_id = farm
      
      utc_dt = datetime.datetime.utcnow().replace(tzinfo=utc)
      me_dt = datetime.datetime(1988, 6, 9, 12, 00, tzinfo=utc)
      ec_dt = ec_tz.normalize(utc_dt.astimezone(ec_tz))

      match = re.search(MarketPlace.Trade.re_creation_datetime, utime)
      if match:
        ec_creation_datetime = ec_tz.localize(
          datetime.datetime(
            ec_dt.year, ec_dt.month, int(match.group(1)), int(match.group(2)), 
            int(match.group(3))
          )
        )

        self.creation_datetime = utc.normalize(
          ec_creation_datetime.astimezone(utc)
        )
      else:
        self.creation_datetime = me_dt
 
      match = re.search(MarketPlace.Trade.re_delivery_date, adate['text'])
      if match:
        ec_delivery_date = ec_tz.localize(
          datetime.datetime(ec_dt.year, ec_dt.month, int(match.group(1)))
        )
        utc_delivery_date = utc.normalize(ec_delivery_date.astimezone(utc))
        self.delivery_date = utc_delivery_date.date()
      else:
        self.delivery_date = me_dt.date()
      
      match = re.search(MarketPlace.Trade.re_expiration_time, exp)
      if match:
        delta = datetime.timedelta(
          hours=int(match.group(1)), minutes=int(match.group(2))
        )
        self.expiration_datetime = utc_dt + delta
      else:
        self.expiration_datetime = me_dt
        
      self.prices = []
      if price40 != "":
        self.prices.append(self.Price("1", price40))
      if price50 != "":
        self.prices.append(self.Price("2", price50))
      if price60 != "":
        self.prices.append(self.Price("4", price60))
      if price70 != "":
        self.prices.append(self.Price("8", price70))
      if price80 != "":
        self.prices.append(self.Price("16", price80))
      if price90 != "":
        self.prices.append(self.Price("32", price90))
      if price100 != "":
        self.prices.append(self.Price("64", price100))
      if price100p != "":
        self.prices.append(self.Price("128", price100p))

      try:
        self.hb = Decimal(hb)
      except InvalidOperation:
        self.hb = 0.0

    class Price(object):
      def __init__(self, size_id=None, price=0.0):
        self.size_id = size_id
        try:
          self.price = Decimal(price)
        except InvalidOperation:
          self.price = 0.0

class Messages():
  class UnreadCount(object):
    def __init__(self, unreadCount=None, balance=None):
      self.balance = balance
      if unreadCount is not None:
        try:
          self.all = int(unreadCount['all'])
        except (KeyError, ValueError):
          self.all = None
        try:
          self.support = int(unreadCount['support'])
        except (KeyError, ValueError):
          self.support = None
        try:
          self.system = int(unreadCount['system'])
        except (KeyError, ValueError):
          self.system = None
      else:
        self.all = None
        self.support = None
        self.system = None

class Log(object):
  pass
 
class Filters(object):
  pass 

class Requests():
  class FilterCounters(object):
    def __init__(self, farm=None, variety=None, type=None, size=None):
      self.farms = []
      self.varieties = []
      self.types = []
      self.sizes = []

      if farm is not None:
        self.farms = [self.Counter(k, **v) for k, v in farm.items()]
      if variety is not None:
        self.varieties = [self.Counter(k, **v) for k, v in variety.items()]
      if type is not None:
        self.types = [self.Counter(k, **v) for k, v in type.items()]
      if size is not None:
        self.sizes = [self.Counter(k, **v) for k, v in size.items()]

    class Counter(object):
      def __init__(self, id, bc, sc):
        self.id = id
        try:
          self.bc = int(bc)
        except ValueError:
          self.bc = None
        try:
          self.sc = int(sc)
        except ValueError:
          self.sc = None

  class LastOffers(object):
    def __init__(self, count=0, list=None):
      self.offers = []
      if count > 0:
        self.offers = [self.Offer(**o) for o in list]

    class Offer(object):
      def __init__(self, datetime, short_date, date, farm_name, title, hb, color):
        self.datetime = datetime
        self.short_date = short_date
        self.date = date
        self.farm_name = farm_name
        self.title = title
        self.hb = hb
        self.color = color

  class GetPlatformList(object):
    def __init__(self, request=None):
      self.platfoms = []
      if request is not None:
        self.platforms = [self.Platform(id, name) for id, name in request.items()]

    class Platform(object):
      def __init__(self, id, name):
        self.id = id
        self.name = name

class Handbook(object):
  def __init__(self, lang=None, farm=None, size=None, variety=None, type=None,
               sort=None, trademark=None):
    self.farms = []
    self.types = []
    self.varieties = []
    self.sizes = []
    self.sorts = sort

    if farm is not None:
      for id, name in farm.items():
        try:
          self.farms.append(self.Farm(id, name, trademark[id]))
        except KeyError:
          self.farms.append(self.Farm(id, name, None))
    if type is not None:
      self.types = [self.Type(id, name) for id, name in type.items()]
    if variety is not None:
      self.varieties = [self.Variety(id, name) for id, name in variety.items()]
    if size is not None:
      self.sizes = [self.Size(id, value) for id, value in size.items()]

  class Farm(object):
    def __init__(self, id, name, trademark):
      self.id = id
      self.name = name
      self.trademark = trademark

  class Type(object):
    def __init__(self, id, name):
      self.id = id
      self.name = name
      
  class Variety(object):
    re_picture_link = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"\s+(?:[^>]*?\s+)?data-title="([^"]*)"'

    def __init__(self, id, content):
      self.id = id
      self.pictures = []

      lines = content.split('\n')
      for l in lines:
        l = l.strip()
        match = re.search(Handbook.Variety.re_picture_link, l)
        if match:
          self.name = match.group(2)
          self.pictures.append(match.group(1))
        else:
          self.name = l

  class Size(object):
    def __init__(self, id, value):
      self.id = id
      self.value = value
