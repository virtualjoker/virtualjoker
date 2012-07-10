# chars.py
#
# model: Char
# function: create_char(clients.Client, place, online=True)


from places import Place
from google.appengine.ext import db


class Char(db.Model):
  """ Char Model
      nothing about """
  
  @property
  def id(self):
    return str(self.key())
  
  # What type of object it is
  type = 'char'
  # List of all properties, propierty 'id' auto added
  properties_list = ['type', 'active', 'online', 'x', 'y', 'place']
  # Status : active or not
  active = db.BooleanProperty(default=True)
  # It is online or not
  online = db.BooleanProperty(default=True)
  
  
  # Place IN TEST
  place = db.ReferenceProperty(reference_class=Place)
  # Position (x, y)
  x = db.IntegerProperty(required=True)
  y = db.IntegerProperty(required=True)
  
  
  # timestamp is updated on create
  created = db.DateTimeProperty(auto_now_add=True)
  # timestamp is updated on every refresh
  last_modified = db.DateTimeProperty(auto_now=True)
  
  
  def get_attrs(self):
    return  {
              'id':self.id,
              'type':self.type,
              'active':self.active,
              'online':self.online,
              'x': self.x,
              'y': self.y,
              'place':self.place.id
            }


  





# ----------- Start chars mannager functions --------------------------- #
def create_char(place, online=True):
  if not isinstance(place, Place):
    return None # It neet to throws a exeception (first_maps.Map error)
  
  x = place.w/2
  y = place.h/2
  char = Char(place=place, online=online, x=x, y=y)
  char.put()
  return char


