#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Taken from:
# http://code.activestate.com/recipes/576586-dot-style-nested-lookups-over-dictionary-based-dat/
class DictDotLookup(object):
  def __init__(self, obj):
    self.obj = obj

  def __getitem__(self, key):
    return DictDotLookup(self.obj[key])

  def __getattr__(self, key):
    return self[key]

  def get(self, key, default=None):
    try:
      return self[key]
    except (KeyError, IndexError):
      return default

  def __call__(self):
    return self.obj
