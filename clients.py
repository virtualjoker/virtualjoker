# clients.py
#
# model: Client
# function: create_client(user, first_map = None, logged=True)
# function: get_char(user) # One user, or a list of it

from chars import Char

from google.appengine.ext import db
from google.appengine.api.users import User


class Client(db.Model):
  """ Client Model
      nothing about """
  
  @property
  def id(self):
    return str(self.key())
  
  # Status : active or not
  active = db.BooleanProperty(default=True)
  # User owner
  user = db.UserProperty(required=True)
  # Channel token
  channel_token = db.StringProperty()
  
  
  char = db.ReferenceProperty(reference_class=Char)
  
  # date of the last update
  # when user log set min datetime, to get all updates
  last_update = db.DateTimeProperty()
  
  # timestamp is updated on create
  created = db.DateTimeProperty(auto_now_add=True)
  # timestamp is updated on every refresh
  last_modified = db.DateTimeProperty(auto_now=True)
  




# ----------- Start client auxiliar functions --------------------------- #
def get_client(user, create = False):
  """ This function will create a new char if not exist """
  query = db.Query(Client)
  query.filter('active =', True)
  query.filter('user =', user)
  client = query.get()
  if client:
    return client
  elif not create:
    return None
  else:
    if not isinstance(user, User):
      return None # Here i need to return
    
    client = Client(user=user)
    client.put()
    return client

