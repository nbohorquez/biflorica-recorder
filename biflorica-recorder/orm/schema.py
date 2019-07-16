#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Type(Base):
  __tablename__ = 'type'

  # Columns
  id = Column(String(255), primary_key=True)
  name = Column(String(255), nullable=False)

  # Properties
  varieties = relationship(
    'Variety', backref='type', primaryjoin='Variety.type_id==Type.id'
  )

  def __init__(self, id=None, name=None):
    self.id = id
    self.name = name

variety_size = Table(
  'variety_size', Base.metadata,
  Column('variety_id', String(255), ForeignKey('variety.id'), primary_key=True),
  Column('size_id', String(255), ForeignKey('size.id'), primary_key=True)
)

class Variety(Base):
  __tablename__ = 'variety'

  # Columns
  id = Column(String(255), primary_key=True)
  name = Column(String(255), nullable=False)
  picture = Column(String(255))
  type_id = Column(String(255), ForeignKey('type.id'))

  def __init__(self, id=None, name=None, type_id=None, pictures=None):
    self.id = id
    self.name = name

    if type_id is not None:
      self.type_id = type_id

    if pictures:
      self.picture = pictures[0]

class Size(Base):
  __tablename__ = 'size'

  # Columns
  id = Column(String(255), primary_key=True)
  value = Column(String(255), nullable=False)
  
  def __init__(self, id=None, value=None):
    self.id = id
    self.value = value

class Farm(Base):
  __tablename__ = 'farm'

  # Columns
  id = Column(String(255), primary_key=True)
  name = Column(String(255), nullable=False)
  trademark = Column(String(255))

  def __init__(self, id=None, name=None, trademark=None):
    self.id = id
    self.name = name
    self.trademark = trademark

class Trade(Base):
  __tablename__ = 'trade'

  # Columns
  id = Column(String(255), primary_key=True)
  guid = Column(String(255), primary_key=True)
  hash = Column(String(255), primary_key=True)
  color = Column(String(255), ForeignKey('color.value'), nullable=False)
  type_id = Column(String(255), ForeignKey('type.id'), nullable=False)
  variety_id = Column(String(255), ForeignKey('variety.id'), nullable=False)
  farm_id = Column(String(255), ForeignKey('farm.id'), nullable=False)
  creation_datetime = Column(DateTime, nullable=False)
  delivery_date = Column(Date, nullable=False)
  expiration_datetime = Column(DateTime, nullable=False)
  hb = Column(Numeric, nullable=False)

  # Properties
  farm = relationship('Farm', primaryjoin='Trade.farm_id==Farm.id')
  type = relationship('Type', primaryjoin='Trade.type_id==Type.id')
  variety = relationship('Variety', primaryjoin='Trade.variety_id==Variety.id')
  prices = relationship(
    'Price', backref='trade', primaryjoin='and_(Trade.id==Price.trade_id, '
    'Trade.guid==Price.trade_guid, Trade.hash==Price.trade_hash)'
  )

  def __init__(self, id=None, guid=None, hash=None, color=None, type_id=None, 
               variety_id=None, farm_id=None, creation_datetime=None, delivery_date=None,
               expiration_datetime=None, prices=[], hb=None):
    self.id = id
    self.guid = guid
    self.hash = hash
    self.color = color
    self.type_id = type_id
    self.variety_id = variety_id
    self.farm_id = farm_id
    self.creation_datetime = creation_datetime
    self.delivery_date = delivery_date
    self.expiration_datetime = expiration_datetime
    self.hb = hb

    for p in prices:
      self.prices.append(Price(id, guid, hash, p.size_id, p.price))

class Price(Base):
  __tablename__ = 'price'

  # Columns
  trade_id = Column(String(255), primary_key=True)
  trade_guid = Column(String(255), primary_key=True)
  trade_hash = Column(String(255), primary_key=True)
  size_id = Column(String(255), ForeignKey('size.id'), primary_key=True)
  price = Column(Numeric, nullable=False)
  
  __table_args__ = (
    ForeignKeyConstraint(
      [trade_id, trade_guid, trade_hash], [Trade.id, Trade.guid, Trade.hash]
    ), {}
  )

  def __init__(self, trace_id=None, trace_guid=None, trace_hash=None, 
               size_id=None, price=None):
    self.trace_id = trace_id
    self.trace_guid = trace_guid
    self.trace_hash = trace_hash
    self.size_id = size_id
    self.price = price

class Color(Base):
  __tablename__ = 'color'

  # Columns
  value = Column(String(255), primary_key=True)
  
  def __init__(self, value=None):
    self.value = value

Farm.offers = relationship(
  'Trade', primaryjoin='and_(Farm.id==Trade.id, Trade.color=="green")',
  foreign_keys=[Trade.id, Trade.color]
)

Farm.bids = relationship(
  'Trade', primaryjoin='and_(Farm.id==Trade.id, Trade.color=="blue")',
  foreign_keys=[Trade.id, Trade.color]
)

Variety.sellers = relationship(
  'Trade', primaryjoin='and_(Variety.id==Trade.variety_id, Trade.color=="green")',
  foreign_keys=[Trade.variety_id, Trade.color]
)

Variety.buyers = relationship(
  'Trade', primaryjoin='and_(Variety.id==Trade.variety_id, Trade.color=="blue")',
  foreign_keys=[Trade.variety_id, Trade.color]
)

Type.sellers = relationship(
  'Trade', primaryjoin='and_(Type.id==Trade.type_id, Trade.color=="green")',
  foreign_keys=[Trade.type_id, Trade.color]
)

Type.buyers = relationship(
  'Trade', primaryjoin='and_(Type.id==Trade.type_id, Trade.color=="blue")',
  foreign_keys=[Trade.type_id, Trade.color]
)
