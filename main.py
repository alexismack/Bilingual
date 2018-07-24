import jinja2
import webapp2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from models import User

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))

class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        individual = users.get_current_user()
        if individual:
            #user is logged in
            log_url = users.create_logout_url('/')
            log_message = 'Log Out'
        if not individual:
            #user is not logged in
            log_url = users.create_login_url('/')
            log_message = 'Log In'
        variables = {
            'individual': individual,
            'log_url': log_url,
            'log_message': log_message,
        }
        self.response.out.write(template.render(variables))


# class Authorize(webapp2.RequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('authorize.html')
#         # self.response.write(template.render())
#         individual = users.get_current_user()
#
#         if individual:
#             #user is logged in
#             log_url = users.create_logout_url('/')
#             log_message = 'Log Out'
#         if not individual:
#             #user is not logged in
#             log_url = users.create_login_url('/')
#             log_message = 'Log In'
#         variables = {
#             'individual': individual,
#             'log_url': log_url,
#             'log_message': log_message,
#         }
#         self.response.out.write(template.render(variables))


class Search(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('search.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render())

class Profiles(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('profiles.html')
        self.response.write(template.render())

class CreateAccount(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('createaccount.html')
        self.response.write(template.render())
        # template = jinja_environment.get_template('createaccount.html')
    def post(self):
        template = jinja_environment.get_template('createaccount.html')
        name = self.request.get("name")
        email = self.request.get("email")
        city = self.request.get("city")
        country = self.request.get("country")
        availability = self.request.get("availability")
        time_span = self.request.get("timespan")
        print(email)
        key = ndb.Key("User", email)
        exists = key.get()
        variables = {'email': email + ' already extists'}
        if exists:
            self.response.write(template.render(variables))
        else:
            user = User(key=key, name=name, email=email, city=city, country=country, availability=availability, time_span=time_span)
            user.put()
            self.redirect('/search')


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/search', Search),
    # ('/authorize', Authorize),
    ('/profiles', Profiles),
    ('/createaccount', CreateAccount)
], debug=True)
