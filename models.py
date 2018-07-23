from google.appengine.ext import ndb

class User(ndb.Model):
    City = ndb.StringProperty(required=True)
    Country = ndb.StringProperty(required=True)
    Availability = ndb.StringProperty(required=True)
    Time Span = ndb.StringProperty(required=True)


print(User.Availability)
