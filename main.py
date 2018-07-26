import jinja2
import webapp2
import os
import json
import base64
from google.appengine.ext import ndb
from google.appengine.api import users
from models import User

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))
search_term = " "

class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        individual = users.get_current_user()
        if individual:
            #user is logged in
            log_url = users.create_logout_url('/')
            log_message = 'Log Out'
            sign_up_url = users.create_login_url('/createaccount')

        if not individual:
            #user is not logged in
            log_url = users.create_login_url('/')
            log_message = 'Log In'
            sign_up_url = users.create_login_url('/createaccount')
        variables = {
            'individual': individual,
            'log_url': log_url,
            'log_message': log_message,
            'sign_up_url': sign_up_url,
        }
        self.response.out.write(template.render(variables))


    def post(self):
        template = jinja_environment.get_template('home.html')
        global search_term
        search_term = self.request.get("search")
        self.redirect('/results')
        my_query = User.query(User.country == search_term).order(User.city).fetch()
        print(my_query)
        counter = 0
        for i in my_query:
            variables["name" + str(counter)] = i.name
            counter = counter + 1
        # self.response.write(template.render())

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


# class Search(webapp2.RequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('search.html')
#         self.response.write(template.render())

    # def post(self):
    #     template = jinja_environment.get_template('results.html')
    #     self.response.write(template.render())

class Profiles(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('profiles.html')
        # self.response.write(template.render())
        current = users.get_current_user()
        if current:
            key = ndb.Key('User', current.email())
            individual = key.get()

            log_url = users.create_logout_url('/')
            log_message = 'Log Out'

            variables = {'name': individual.name,
                        'email': individual.email,
                        'city': individual.city,
                        'country': individual.country,
                        'time_span': individual.time_span,
                        'availability': individual.availability,
                        'log_url': log_url,
                        'log_message': log_message,
                        }
            if individual.image:
                variables['avatar'] = base64.b64encode(individual.image)
            self.response.write(template.render(variables))

        else:
            self.redirect('/')
    def post(self):
        current = users.get_current_user()
        if current:
            key = ndb.Key('User', current.email())
            individual = key.get()
            avatar = self.request.get('avatar')
            individual.image = avatar
            individual.put()
        self.redirect('/profiles')

class Results(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('results.html')
        individual = users.get_current_user()
        if individual:
            #user is logged in
            log_url = users.create_logout_url('/')
            log_message = 'Log Out'
            sign_up_url = users.create_login_url('/createaccount')

        if not individual:
            #user is not logged in
            log_url = users.create_login_url('/')
            log_message = 'Log In'
            sign_up_url = users.create_login_url('/createaccount')
        variables = {
            'individual': individual,
            'log_url': log_url,
            'log_message': log_message,
            'sign_up_url': sign_up_url,
            'search_term': search_term
        }
        self.response.write(template.render(variables))

    def post(self):
        template = jinja_environment.get_template('results.html')
        global search_term
        search_term = self.request.get("search")
        variables = {'search_term': search_term}

        my_query = User.query(User.country == search_term).order(User.city).fetch()
        print(my_query)
        counter = 0
        for i in my_query:

            variables["name" + str(counter)] = i.name
            variables["city" + str(counter)] = i.city
            variables["email" + str(counter)] = i.email
            counter = counter + 1
            print variables
        print variables
            # variable['my_query': my_name]
        self.response.write(template.render(variables))



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
        key = ndb.Key("User", email)
        exists = key.get()
        email_exists = {'email': email + ' already exists'}
        incomplete_message = "Please fill out completely"
        field_empty = {'incomplete_message': incomplete_message}
        if exists:
            self.response.write(template.render(email_exists))
        else:
            if template=="" or name=="" or email=="" or city=="" or country=="" or availability=="" or not time_span:
                self.response.write(template.render(field_empty))
            else:
                user = User(key=key, name=name, email=email, city=city, country=country, availability=availability, time_span=time_span)
                user.put()
                key = ndb.Key("User", email)
                exists = key.get()
                self.redirect('/profiles')



app = webapp2.WSGIApplication([
    ('/', Home),
    # ('/search', Search),
    # ('/authorize', Authorize),
    ('/profiles', Profiles),
    ('/createaccount', CreateAccount),
    ('/results', Results)
], debug=True)
