# listeners.py
#
# model: Listener
# function: create_client(user, first_map = None, logged=True)
# function: get_char(user) # One user, or a list of it

import datetime

from jsonproperty import JsonProperty

from google.appengine.ext import db


class Listener(db.Model):
  """ Listener Model
      nothing about """
  
  @property
  def id(self):
    return str(self.key())
  
  # Status : active or not
  active = db.BooleanProperty(default=True)
  
  # What place is listening
  place = db.ReferenceProperty(required=True)
  # Objects of the screen list
  #object_list = JsonProperty(default={})
  # Objects opdateds
  updates = JsonProperty(default={})
  # date of the last update
  # when user log set min datetime, to get all updates
  last_update = db.DateTimeProperty(default=datetime.datetime.min)
  
  # timestamp is updated on create
  created = db.DateTimeProperty(auto_now_add=True)
  # timestamp is updated on every refresh
  last_modified = db.DateTimeProperty(auto_now=True)
  




# ----------- Start client auxiliar functions --------------------------- #
def add_listener(place):
  """ This function will create a new listener if not exist """
  query = db.Query(Listener, keys_only=True)
  query.filter('active =', True)
  query.filter('place =', place)
  listener_key = query.get()
  if listener_key:
    return listener_key
  else:
    listener = Listener(place=place)
    listener.put()
    return listener.key()

