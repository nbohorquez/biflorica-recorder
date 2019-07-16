#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, time, json

from biflorica.commons import config
from commons import DictDotLookup
from objects import Handbook, Messages, Requests, Log, Filters, MarketPlace

API_BASE_URL = config.get('biflorica.api', 'base_url')

class APISession():
  def __init__(self, headers=None):
    self.session = requests.Session()
    self.session.headers.update(headers)

    self.marketplace = self._MarketPlace(self.session)
    self.log = self._Log(self.session)
    self.filters = self._Filters(self.session)
    self.handbook = self._Handbook(self.session)
    self.messages = self._Messages(self.session)
    self.requests = self._Requests(self.session)
    self.users = self._Users(self.session)

  class _MarketPlace():
    URL = API_BASE_URL + config.get('biflorica.api', 'marketplace')
    PARAMS = DictDotLookup(eval("""{
      '_': {
      }, 'contentType': {
        'JSON': 'json'
      }, 'efiltersChecks': {
        'FALSE': 'false',
        'TRUE': 'true'
      }, 'hideCompetitors': {
        'FALSE': 'false',
        'TRUE': 'true'
      }, 'limit': {
        'PAGE': '26'
      }, 'onlyTrusted': {
        'FALSE': 'false',
        'TRUE': 'true'
      }, 'show': {
        'SELLERS': 'sellers',
        'BUYERS': 'buyers',
        'ALL': 'all'
      }, 'sort': {
        'UTIME': 'utime',
        'FARM': 'farm',
        'TYPE': 'type',
        'VARIETY': 'variety',
        'PRICE40': 'price40',
        'PRICE50': 'price50',
        'PRICE60': 'price60',
        'PRICE70': 'price70',
        'PRICE80': 'price80',
        'PRICE90': 'price90',
        'PRICE100': 'price100',
        'PRICE100P': 'price100p',
        'HB': 'hb',
        'EXP': 'exp',
        'ADATE': 'adate'
      }, 'direct': {
        'DESCENDING': 'desc',
        'ASCENDING': 'asc'
      }, 'start': {
        'TOP': '0'
      }, 'farm': {
      }, 'type': {
      }, 'variety': {
      }, 'size': {
      }
    }"""))

    def get(self, start=PARAMS.start.TOP(), 
            limit=PARAMS.limit.PAGE(), 
            sort=PARAMS.sort.UTIME(), 
            direct=PARAMS.direct.DESCENDING(), 
            show=PARAMS.show.ALL(), 
            onlyTrusted=PARAMS.onlyTrusted.FALSE(), 
            hideCompetitors=PARAMS.hideCompetitors.FALSE(), 
            efiltersChecks=PARAMS.efiltersChecks.FALSE(), 
            farm=[], type=[], variety=[], size=[]):
      # The '_' parameter is composed of 13 ditigs:
      # *- 10 at the beginning for the UNIX timestamp (seconds since 1/1/1970)
      # *- 3 ending numbers which I believe are just miliseconds
      payload = {
        '_': '{0}'.format(int(time.time()*1000)),
        'contentType': APISession._MarketPlace.PARAMS.contentType.JSON(),
        'efiltersChecks': efiltersChecks,
        'hideCompetitors': hideCompetitors,
        'limit': limit,
        'onlyTrusted': onlyTrusted,
        'show[]': show,
        'sort': sort,
        'direct': direct,
        'start': start,
        'farm[]': farm,
        'type[]': type,
        'variety[]': variety,
        'size[]': size
      }
      r = self._session.get(APISession._MarketPlace.URL, params=payload)
      return MarketPlace(**r.json()['data'])

    def __init__(self, session=None):
      self._session = session

  class _Log():
    URL = API_BASE_URL + config.get('biflorica.api', 'log')
    PARAMS = DictDotLookup(eval("""{
      '_': {
      }, 'contentType': {
        'JSON': 'json'
      }, 'limit': {
        'PAGE': '26'
      }, 'start': {
        'TOP': '0'
      }
    }"""))

    def __init__(self, session=None):
      self._session = session

    def get(self, start=PARAMS.start.TOP(), limit=PARAMS.limit.PAGE()):
      payload = {
        '_': '{0}'.format(int(time.time()*1000)),
        'contentType': APISession._Log.PARAMS.contentType.JSON(),
        'start': start,
        'limit': limit
      }
      r = self._session.get(APISession._Log.URL, params=payload)
      return Log(**r.json()['data'])

  class _Filters():
    URL = API_BASE_URL + config.get('biflorica.api', 'filters')
    PARAMS = DictDotLookup(eval("""{'_': {}}"""))

    def __init__(self, session=None):
      self._session = session

    def get(self):
      payload = {
        '_': '{0}'.format(int(time.time()*1000)),
      }
      r = self._session.get(APISession._Filters.URL, params=payload)
      return Filters(**r.json()['data'])

  class _Handbook():
    URL = API_BASE_URL + config.get('biflorica.api', 'handbook')
    PARAMS = DictDotLookup(eval("""{
      '_': {
      }, 'sections': {
        'FARM': 'farm',
        'SIZE': 'size',
        'VARIETY': 'variety',
        'TYPE': 'type',
        'SORT': 'sort',
        'TRADEMARK': 'trademark',
        'LANGUAGE': 'lang'
      }
    }"""))

    def __init__(self, session=None):
      self._session = session

    def get(self, sections=[PARAMS.sections.LANGUAGE()]):
      payload = {
        '_': '{0}'.format(int(time.time()*1000)),
        'sections[]': sections
      }
      r = self._session.get(APISession._Handbook.URL, params=payload)
      return Handbook(**r.json()['data'])

  class _Messages():
    def __init__(self, session):
      self._session = session
      self.unreadCount = self._UnreadCount(session)

    class _UnreadCount():
      URL = API_BASE_URL + config.get('biflorica.api.messages', 'unread_count')
      PARAMS = DictDotLookup(eval("""{'_': {}}"""))

      def __init__(self, session=None):
        self._session = session

      def get(self):
        payload = {'_': '{0}'.format(int(time.time()*1000))}
        r = self._session.get(APISession._Messages._UnreadCount.URL, params=payload)
        return Messages.UnreadCount(**r.json()['data'])

  class _Users():
    def __init__(self, session):
      self._session = session
      self.login = self._Login(session)
      self.logout = self._Logout(session)

    class _Login():
      URL = API_BASE_URL + config.get('biflorica.api.users', 'login')
      PARAMS = DictDotLookup(eval("""{'login':{}, 'password':{}}"""))

      def __init__(self, session=None):
        self._session = session

      def post(self, user=None, password=None):
        from biflorica.platform import Login as PlatformLogin
        # This page does not use encryption and sends the credentials in plain text!
        # The name of the input fields are not what they are reported in the html.
        # I had to look at the actual request in Firebug to see the real names of the
        # fields.
        if user is None:
          user = config.get('biflorica.platform', 'login')
          password = config.get('biflorica.platform', 'password')

        payload = {'login': user, 'password': password}
        # First get the cookies in the html site, we'll need them
        r = self._session.get(PlatformLogin.URL)
        tmp = r.content
        # The real login is in here, in the API login
        r = self._session.post(APISession._Users._Login.URL, data=payload)
        tmp = r.content

    class _Logout():
      URL = API_BASE_URL + config.get('biflorica.api.users', 'logout')
      PARAMS = DictDotLookup(eval("""{}"""))

      def __init__(self, session=None):
        self._session = session

      def get(self):
        r = self._session.get(APISession._Users._Logout.URL)
        tmp = r.content

  class _Requests():
    def __init__(self, session):
      self._session = session
      self.filterCounters = self._FilterCounters(session)
      self.lastOffers = self._LastOffers(session)
      self.getPlatformList = self._GetPlatformList(session)

    class _FilterCounters():
      URL = API_BASE_URL + config.get('biflorica.api.requests', 'filter_counters')
      PARAMS = DictDotLookup(eval("""{'_': {}}"""))

      def __init__(self, session=None):
        self._session = session

      def get(self):
        payload = {'_': '{0}'.format(int(time.time()*1000))}
        r = self._session.get(APISession._Requests._FilterCounters.URL, params=payload)
        return Requests.FilterCounters(**r.json()['data'])

    class _LastOffers():
      URL = API_BASE_URL + config.get('biflorica.api.requests', 'last_offers')
      PARAMS = DictDotLookup(eval("""{
        '_': {
        }, 'contentType': {
          'JSON': 'json'
        }, 'limit': {
          'PAGE': '26'
        }, 'start': {
          'TOP': '0'
        }
      }"""))

      def __init__(self, session=None):
        self._session = session

      def get(self, start=PARAMS.start.TOP(), limit=PARAMS.limit.PAGE()):
        payload = {
          '_': '{0}'.format(int(time.time()*1000)),
          'contentType': APISession._Requests._LastOffers.PARAMS.contentType.JSON(),
          'start': start,
          'limit': limit
        }
        r = self._session.get(APISession._Requests._LastOffers.URL, params=payload)
        return Requests.LastOffers(**r.json()['data'])

    class _GetPlatformList():
      URL = API_BASE_URL + config.get('biflorica.api.requests', 'get_platform_list')
      PARAMS = DictDotLookup(eval("""{'_': {}}"""))

      def __init__(self, session=None):
        self._session = session

      def get(self):
        payload = {'_': '{0}'.format(int(time.time()*1000))}
        r = self._session.get(APISession._Requests._GetPlatformList.URL, params=payload)
        return Requests.GetPlatformList(**r.json()['data'])

"""
THESE ARE THE FUNCTIONS AVAILABLE IN THE API:

Marketplace
===========
Get the juice of all this: offers and bids!
url = '+marketPlace'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
  'contentType': (json, ?),
  'efiltersChecks':'false',
  'hideCompetitors': (true, false),
  'limit': (n) Limit the response to n rows/entries,
  'onlyTrusted': (true, false),
  'show[]': ['sellers', 'buyers', 'all'],
  'sort': [
    'utime',
    'farm',
    'type',
    'variety',
    'price40',
    'price50',
    'price60', 
    'price70', 
    'price80', 
    'price90', 
    'price100', 
    'price100p',
    'hb',
    'exp',
    'adate'
  ],
  'direct': ['desc', 'asc']
  'start': (n) Starting index,
  'farm[]': [] List of farms id's to filter,
  'type[]': [] List of types id's to filter,
  'variety[]': [] List of varieties id's to filter,
  'size[]': [] List of sizes id's to filter
}
response = {
  'query': '',
  'infoMessage': [],
  'errors': [],
  'data': {
    'count': (n)
    'list': [
      {
        "guid":"13492053",
        "canBeChosen":false,
        "adate":{               # Airport delivery date
          "type":"div",
          "text":"21 Sat",
          "classId":""
        },
        "exp":"03:11",
        "farm":"46",
        "hb":"1.0",
        "id":"2003-R-0",
        "utime":"20 15:43",
        "type":"1",
        "is_standing":"",
        "variety":"33",
        "price40":"",
        "price50":"",
        "price60":"0.35",
        "price70":"",
        "price80":"",
        "price90":"",
        "price100":"",
        "price100p":"",
        "buttons":[ ],
        "color":"blue",
        "hash":"0d6b5b41ad906b5d45a63c3267a3b5b8"
      }, {
        u'color':u'green',
        u'price90':u'',
        u'adate':{
          u'classId':u'',
          u'text':u'20 Fri',
          u'type':u'div'
        },
        u'price100':u'',
        u'guid':u'13490144',
        u'id':u'1903-F-52181069',
        u'price60':u'',
        u'variety':u'173',
        u'canBeChosen':False,
        u'price100p':u'',
        u'buttons':[ ],
        u'price80':u'',
        u'type':u'1',
        u'hash':u'2c6dfc33428cc605dafe3803f2179170',
        u'farm':u'46',
        u'hb':u'1.0',
        u'is_standing':u'',
        u'utime':u'19 15:39', 
        u'price40':u'',
        u'exp':u'23:46', 
        u'price70':u'',
        u'price50':u'0.50'
      },
      ...
    ]
  },
  'fieldsErrors': []
}

Messages - UnreadCount
======================
Returns the unread messages in the tray
url = '+messages/unreadCount'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
}
response = {
  'query':'',
  'data':{
    'unreadCount':{
      'all':(n),
      'support':(n),
      'system':(n)
    },
    'balance':($%.2f)
  },
  'infoMessage':[],
  'errors':[],
  'fieldsErrors':[]
}

Log
===
Get logging information from the server to show to the user
url = '+log/'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
  'contentType': (json, ?)
  'limit': (n) Limit the response to n rows/entries,
  'start': (n) Starting index
}
response = {
  'query':'limit=26&start=0&contentType=json',
  'data': {
    'list':[],
    'count':(n),
    'has_critical':(true, false)
  },
  'infoMessage':[],
  'errors':[],
  'fieldsErrors':[]
}

Filters
=======
Don't know yet
url = '+filters/'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
}
response = {
  'query':'',
  'data':{
    'count':(n),
    'list':[]
  },
  'infoMessage':[],
  'errors':[],
  'fieldsErrors':[]
}

Requests - FilterCounters
=========================
Don't know yet
url = '+requests/filterCounters/'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
}
response = {
  'query':'',
  'data':{
    'farm': {
      '(id)': {         Id of the farm
        'bc':(n),       Bids
        'sc':(n)        Offers
      },
      ...
    },
    'variety': {
      '(id)': {         Id of the variety
        'bc':(n),       Bids
        'sc':(n)        Offers
      },
      ...
    }, 
    'type': {
      '(id)': {         Id of the type
        'bc':(n),       Bids
        'sc':(n)        Offers
      },
      ...
    },
    'size': {
      '(id)':{          Id of the size
        'bc':(n),       Bids
        'sc':(n)        Offers
      },
      ...
    }
  },
  'infoMessage':[],
  'errors':[],
  'fieldsErrors':[]
}

Requests - LastOffers
=====================
Get last offers in the marketplace
url = '+requests/lastOffers'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
  'contentType': (json, ?)
  'limit': (n) Limit the response to n rows/entries,
  'start': (n) Starting index
}
response = {
  'query':'limit=26&start=0&contentType=json',
  'data':{
    'count':2,
    'list':[
      {
        'datetime':'15:17:38',
        'short_date':'18  15:17:<span>38<\/span>',
        'date':'18 Mar 2015, 15:17:38',
        'farm_name':'QUALISA',
        'title':{
            'type':'a',
            'href':'#stayhere',
            'onclick':'javascript:filters.applyLastOffersFarm(46);',
            'text':'QUALISA'
        },
        'hb':'<hb>1<\/hb> HB',
        'color':'white'
      },{
        'datetime':'11:36:46',
        'short_date':'18  11:36:<span>46<\/span>',
        'date':'18 Mar 2015, 11:36:46',
        'farm_name':'CANANV',
        'title':{
          'type':'a',
          'href':'#stayhere',
          'onclick':'javascript:filters.applyLastOffersFarm(164);',
          'text':'CANANV'
        },
        'hb':'<hb>4<\/hb> HB',
        'color':'white'
      }
    ]
  },
  'infoMessage':[],
  'errors':[],
  'fieldsErrors':[]
}

Requests - GetPlatformsList
===========================
Lists the countries were this system is avaliable.
url = '+requests/getPlatformsList/'
params = {
  '_': 13-digit UNIX timestamp including miliseconds
}
response = {
  'query': '',
  'data': {
    'request': {
      '1':'Ecuador',
      '2':'Colombia',
      '3':'Spain'
    }
  },
  'infoMessage': [],
  'errors': [],
  'fieldsErrors': []
}

Handbook
========
Retrieves textual information visible to the user. Localized by language?
url = '+handbook/'
params = {
  '_': 13-digit UNIX timestamp including miliseconds,
  'sections[]': At least one [farm, size, variety, type, sort, trademark, lang]
}
response = {
  'query': "sections%5B%5D=lang&sections%5B%5D=farm&sections%5B%5D=size&sections%5B%5D=variety&sections%5B%5D=type&sections%5B%5D=sort&sections%5B%5D=trademark"",
  'data': {
    'lang': {
      "titles":{
        "alert":"Alert!",
        "error":"Error!",
        "date":"Date",
        "next":"More",
        "collapse":"Collapse"
      },
      "alert_text":{
        "confirm_deals_cancel":"Are you sure you want to cancel the deals?",
        "confirm_delete_price_item":"Are you sure you want to delete the selected items from your price list?",
        "EmptyVarienty":"All {type} varieties have already been added to your price list.<br \/>\nPlease <a target=\"_blank\" href=\"\/marketPlace\/messages\/?type=new_variety#add_new\">let us know<\/a> if your variety is not available as an option.",
        "addSort":"<a target=\"_blank\" href=\"\/marketPlace\/messages\/?type=new_variety#add_new\">Add<\/a> a new variety",
        "TransportChanged":"TransportChanged_seller",
        "MarkerChanged":"MarkerChanged_seller",
        "TransportChangedAndMarkerChanged":"TransportChangedAndMarkerChanged_seller"
      },
      "help":{
        "place":"These indexes help compare prices. The index 1 corresponds to the group of the cheapest flowers, while 5 corresponds to the most expensive one.",
        "in_grid_selected_first_not_selected_current_value":"Select a {type} in the left box.",
        "in_grid_selected_middle_not_selected_current_value":"Select a {type} in the middle box.",
        "text_selected_first_farm_not_selected_current_value":"The farms are arranged in order of the amount of flowers that they sold in the BiFlorica trading system in the selected time period.",
        "text_selected_first_size_not_selected_current_value":"The flowers are arranged in order of the sizes that were sold most often by all of the producers in the BiFlorica trading system in the selected time period.",
        "text_selected_first_variety_not_selected_current_value":"The flowers are arranged in order of the varieites that were sold most often by all of the producers in the BiFlorica trading system in the selected time period.",
        "text_selected_first_farm_selected_current_value_middle_selected_variety":"The flowers are arranged in order of the {type} that were sold most often by the {farm} farm.",
        "text_selected_first_farm_selected_current_value_middle_selected_size":"The flowers are arranged in order of the {type} that were sold most often by the {farm} farm.",
        "text_selected_first_variety_selected_current_value_middle_selected_farm":"The farms are arranged in order of the amount of {variety} flowers they sold.",
        "text_selected_first_variety_selected_current_value_middle_selected_size":"The sizes are arranged in order of the amount of {variety} flowers sold by all of the farms.",
        "text_selected_first_size_selected_current_value_middle_selected_farm":"The farms are arranged in order of the amount of {size}cm flowers they sold.",
        "text_selected_first_size_selected_current_value_middle_selected_variety":"The varieties are arranged in order of the amount of {size} flowers sold by all of the farms.",
        "text_selected_middle_variety_selected_current_value_third_selected_size":"The sizes are arranged in order of the amount of {variety} flowers sold by the {farm} farm.",
        "text_selected_middle_variety_selected_current_value_third_selected_farm":"The farms are arranged in order of the amount of {variety}-{size}cm flowers they sold.",
        "text_selected_middle_size_selected_current_value_third_selected_variety":"The varieties are arranged in order of the amount of {size}cm flowers sold by the {farm} farm.",
        "text_selected_middle_size_selected_current_value_third_selected_farm":"The farms are arranged in order of the amount of {variety}-{size}cm flowers they sold.",
        "can_delete_only_off_requests_text_for_order":"Orders that contain only <i>OFF market<\/i> and\/or <i>Expired<\/i> requests can be deleted.\r\nOrders that contain <i>ON market<\/i> requests and\/or <i>Deals<\/i> cannot be deleted.",
        "are_you_sure_to_delete_order":"Are you sure you want to delete \r\nthe selected orders?"
      },
      "tooltips":{
        "marketPlacePrice":"marketPlacePrice",
        "UpdatedTime":"Updated time",
        "rollWeekly":"ROLLING WEEKLY(currency_code)",
        "next_d":"NEXT DAY INCREMENT (currency_code)",
        "lastUpdate":"LAST UPDATE",
        "bayersId":"BUYER'S ID",
        "agentId":"AGENT'S ID",
        "producersTrademark":"PRODUCER'S TRADEMARK",
        "noDeal7day":"You don't have deals with the delivery dates in the last 7 days.",
        "ADTChange":"If the deal is concluded before the airport delivery time,<br>\nthe sold products will be delivered to the airport this day.<br>\nIf the deal is concluded after the airport delivery time,<br>\nthe sold products will be delivered to the airport the next day.",
        "create_order_for_copy":"There are currently no active orders associated with your account.\r\n<br \/>A new order must be created, then you can copy requests there."
      },
      "grids":{
        "DAY,TIME":"DAY,TIME",
        "TYPE":"TYPE",
        "HB":"HB",
        "VARIETY":"VARIETY",
        "PRICE BY CM ($)":"PRICE PER STEM ($)",
        "AIRPORT":"AIRPORT",
        "DELIV.":"DELIV.",
        "FARM":"FARM",
        "CREATED ON":"CREATED ON",
        "HALF BOX":"HALF BOXES",
        "FILTER NAME":"FILTER NAME",
        "SIZE":"SIZE",
        "COMPANY":"COMPANY",
        "CARGO":"CARGO",
        "TRANSPORT":"TRANSPORT",
        "AGENCY":"AGENCY",
        "UPDATE":"UPDATE",
        "ID":"ID",
        "BUYER'S NAME":"BUYER'S NAME",
        "AGENT'S NAME":"AGENT",
        "AGENT":"AGENT",
        "SUB.NAME":"SUBBUYER",
        "SUBMARK":"MARK",
        "LEFT($)":"LEFT($)",
        "LEFT":"BALANS($)",
        "LEFT2":"BALANS(\u20ac)",
        "WEEKLY($)":"WEEKLY($)",
        "NEXT D.($)":"NEXT D.($)",
        "MARK":"MARK",
        "STATUS":"STATUS",
        "TRUST":"TRUST",
        "DEALS IN":"DEALS IN",
        "2 DAYS (HB)":"2 DAYS (HB)",
        "PRODUCER'S \\ AGENT'S TRUST":"PRODUCER'S \\ AGENT'S TRUST",
        "SUBMARK.NAME":"MARK",
        "SUBMARK.COMMENT":"COMMENT",
        "ANY":"ANY",
        "Me":"&lt;Me&gt;",
        "All partnerships":"All partnerships",
        "REQUEST.UPD":"UPD.",
        "ALL\/ DEAL":"ALL\/ DEAL",
        "SUBM":"MARK",
        "REQUEST.EXP":"EXP",
        "REQUEST.INF":"INF",
        "REQUEST.IND":"IND",
        "REQUEST.ORDER":"ORDER",
        "ORDER NAME":"ORDER NAME",
        "ORDER.ABBR":"ABBR",
        "SHIPMENT DATE":"SHIPMENT DATE",
        "ORDER.ALL":"ALL",
        "ORDER.ON":"ON",
        "ORDER.DEALS":"DEALS",
        "ORDER.OFF":"OFF",
        "ORDER.EXP":"EXP",
        "message.date":"DATE",
        "message.from":"FROM",
        "message.subject":"SUBJECT",
        "grid.nodata":"No data available. Please check the filter settings.",
        "EVENT":"EVENT",
        "INFO.COMMENT":"COMMENT",
        "DATE, TIME":"DATE, TIME",
        "New filter":"New filter",
        "ANALYTICS.NAME":"NAME",
        "ANALYTICS.PRICE":"PRICE&nbsp;",
        "ANALYTICS.variety":"VARIETY",
        "ANALYTICS.farm":"FARM",
        "ANALYTICS.size":"SIZE",
        "ANALYTICS.title_variety":"variety",
        "ANALYTICS.title_farm":"farm",
        "ANALYTICS.title_size":"analytics.title_size",
        "DEAL.TRANSACTED_ON":"TRANSACTED ON",
        "DEAL.PRICE":"PRICE PER ST.($)",
        "DEAL.TOTAL":"PRICE ($)",
        "DEAL.TAX":"COMMISS ($)",
        "DEAL.TRANSPORT_AGENCY":"TRANSPORT AGENCY",
        "DEAL.AIRPORT_DELIVERY":"AIRPORT DELIVERY",
        "Reset all filters":"Reset all filters",
        "REQUEST.COMMISSION":"commiss",
        "REQUEST.TOTAL":"total",
        "REQUEST.FLCOUNT":"Stems"
      }
    }
    "farm":{
      "(id)":"(name shown)",
      ...
    },
    "size":{
      "1":"40",
      "2":"50",
      "4":"60",
      "8":"70",
      "16":"80",
      "32":"90",
      "64":"100",
      "128":"100p"
    },
    "variety": {
      "718":" LA Green 3\/5",
      "372":"
        <a href=\"\/images\/flowers\/sort_file_372_24_02_2015_41173.jpg\" data-lightbox=\"image-372!\" data-title=\"3D\">3D<\/a>
        <a href=\"\/images\/flowers\/sort_file_372_24_02_2015_170774.jpg\" data-lightbox=\"image-372!\" data-title=\"3D\"><\/a>
      ",
      "655":"Abril",
      "210":"
        <a href=\"\/images\/flowers\/sort_file_210_15_02_2015_172853.jpg\" data-lightbox=\"image-210!\" data-title=\"Absurda\">Absurda<\/a>
        <a href=\"\/images\/flowers\/sort_file_210_15_02_2015_433916.jpg\" data-lightbox=\"image-210!\" data-title=\"Absurda\"><\/a>
        <a href=\"\/images\/flowers\/sort_file_210_15_02_2015_660819.jpg\" data-lightbox=\"image-210!\" data-title=\"Absurda\"><\/a>
        <a href=\"\/images\/flowers\/sort_file_210_15_02_2015_390252.jpg\" data-lightbox=\"image-210!\" data-title=\"Absurda\"><\/a>
        <a href=\"\/images\/flowers\/sort_file_210_15_02_2015_948212.jpg\" data-lightbox=\"image-210!\" data-title=\"Absurda\"><\/a>
      ",
      ...
    }
    "type":{
      "(id)":"(name of flower)",
      ...
    }
    "sort":[
      "Farm <s>\u2192<\/s> Variety <s>\u2192<\/s> Size",
      "Variety <s>\u2192<\/s> Size <s>\u2192<\/s> Farm"
    ],
    "trademark":{
      "(id)":"(legal name/trademark)",
    }
  },
  "infoMessage":[ ],
  "errors":[ ],
  "fieldsErrors":[ ]
}
"""
