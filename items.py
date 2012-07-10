# items.py
#
# model: Item

from chars import Char
from places import Place

from google.appengine.ext import db

class Item(db.Model):
  """ Item Model
      NOT IMPLEMENTED YET !!! """
  
  @property
  def id(self):
    return str(self.key())
  
  # What type of object it is
  type = 'item'
  # List of all properties, propierty 'id' auto added
  properties_list = ['type', 'active', 'x', 'y', 'place']
  # Status: active or not
  active = db.BooleanProperty(default=True)
  # Where is the item
  # !!! NOT IMPLEMENTED YET, this can only be in one place, that is not right
  place = db.ReferenceProperty(reference_class=Place)
  # Chars owner
  char = db.ReferenceProperty(reference_class=Char)
  
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
              'x': self.x,
              'y': self.y,
              'place':self.place.id
            }


