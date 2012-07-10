# places.py
#
# model: Place
# function: first_place()

import datetime

from google.appengine.ext import db

FIRST_PLACE_NAME = 'first_place'
FIRST_PLACE_W = 16
FIRST_PLACE_H = 16


class Place(db.Model):
  """ Place Model
      nothing about """
  
  @property
  def id(self):
    return str(self.key())
  
  # What type of object it is
  type = 'place'
  # List of all properties, propierty 'id' auto added
  properties_list = ['type', 'active', 'name', 'w', 'h', 'ground']
  # Status: active or not
  active = db.BooleanProperty(default=True)
  # Place name
  name = db.StringProperty(required=True)
  
  # Position (x, y)
  x = db.IntegerProperty(required=True)
  y = db.IntegerProperty(required=True)
  
  # Size (width, height)
  w = db.IntegerProperty(required=True)
  h = db.IntegerProperty(required=True)
  ground = db.StringListProperty(required=True)
  
  # timestamp is updated on create
  created = db.DateTimeProperty(auto_now_add=True)
  # timestamp is updated on every refresh
  last_modified = db.DateTimeProperty(auto_now=True)
  
  def get_attrs(self):
    return  {
              'id':self.id,
              'type':self.type,
              'active':self.active,
              'name': self.name,
              'w': self.w,
              'h': self.h,
              'ground':self.ground
            }



# ----------- Start places mannager ----------------
# This function will not work in production
def first_place():
  """ This function will return the first place """
  
  query = db.Query(Place)
  query.filter('name = ', FIRST_PLACE_NAME)
  place = query.get()
  if place:
    return place
  else:
    # Build the default ground
    ground = []
    for i in range(FIRST_PLACE_W * FIRST_PLACE_H):
      ground.append('default')
    place = Place(
                name=FIRST_PLACE_NAME,
                x=0, y=0, # first_place default on the center
                w=FIRST_PLACE_W, h=FIRST_PLACE_H,
                ground=ground
             )
    place.put()
    return place


