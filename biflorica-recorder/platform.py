#!/usr/bin/env python
# -*- coding: utf-8 -*-

from biflorica.commons import config

PLATFORM_BASE_URL = config.get('biflorica.platform', 'base_url')

class Login():
  URL = PLATFORM_BASE_URL + config.get('biflorica.platform', 'login_url')
