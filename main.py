import jinja2
import webapp2
import os
import json
from google.appengine.ext import ndb
# from models import User

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))

class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())
# class Authentication(webapp2.RequestHandler):
#     def get(self):
#         params = {
#         'api_key': ''
#         'q':
class Search(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('search.html')
        self.response.write(template.render())
class Results(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render())
app = webapp2.WSGIApplication([
    ('/', Home),
    # ('/Profile', Profile),
    ('/search', Search),
    ('/results', Results),
], debug=True)
