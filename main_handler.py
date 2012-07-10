# main_handler.py

import os
import datetime

from clients import get_client
from chars import create_char
from places import first_place
from aux import is_development

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_PATH,'template')
INDEX_PATH = os.path.join(TEMPLATE_PATH, 'main.html')
  
  
class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      # Sux create fast solution
      client = get_client(user=user, create=True)
      
      if not client.char:
        # Sux create fast first map
        place = first_place()
        client.char = create_char(place=place)
      
      else:
        # Put char online and atualize his last_modified
        # to do not become ofline again
        client.char.online = True
        client.char.put()
      
      
      # Client need to update all the screen...
      client.last_update = datetime.datetime.min
      client.put()
      
      template_values = {
                          'is_develompent': is_development,
                          'client_id': client.id,
                          'client_char_id': client.char.id,
                          'client_char_place_id': client.char.place.id,
                          'logout_url': users.create_logout_url(self.request.uri),
                        }
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(template.render(INDEX_PATH, template_values))

    

# ----------------------------------------------------------------------- #
application = webapp.WSGIApplication(
    [
      ('/.*', MainHandler)
    ],
    debug = True
  )

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
