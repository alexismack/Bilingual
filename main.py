import jinja2
import webapp2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))

class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())


class Authorize(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('authorize.html')
        self.response.write(template.render())
        individual = users.get_current_user()

        if individual:
            #user is logged in
            log_url = users.create_logout_url('/')
            log_message = 'Sign Out'
        else:
            #user is not logged in
            log_url = users.create_login_url('/')
            log_message = 'Sign In'
        variables = {
            'individual': individual,
            'log_url': log_url,
            'log_message': log_message,
        }
        self.response.out.write(template.render(variables))


class Search(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('search.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/search', Search),
    ('/authorize', Authorize)
], debug=True)
