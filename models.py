import logging
import os
import jinja2
import webapp2
import json
import urllib2
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb


class User(ndb.Model):
    city = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)
    availability = ndb.StringProperty(required=True)
    time_span = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    user_id = ndb.StringProperty(required=True)

print(User.Availability)
