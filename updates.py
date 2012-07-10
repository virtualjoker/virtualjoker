# updates.py
#
# model: Update
# function: create_update(user, first_map = None, logged=True)

from jsonproperty import JsonProperty
from places import Place

from google.appengine.ext import db


class Update(db.Model):
  """ Update Model
      nothing about """
  
  # What place needs update
  place = db.ReferenceProperty(reference_class=Place, required=True)
  # Updates to this place
  update = JsonProperty(required=True)
  
  # creation date of update
  datetime = db.DateTimeProperty(auto_now_add=True)


