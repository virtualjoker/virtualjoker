# actions.py
#
# function(action, response)

import datetime

from jsonproperty import JsonProperty

from chars import Char
from items import Item
from aux import add_response
#from aux import distance
from google.appengine.ext import db

# This is the signature of all feeder actions availables
actions_signatures = {
                'move':[int, int],
              }


class Action(db.Model):
  """ Action Model
      nothing about """
  
  # Status : active or not
  active = db.BooleanProperty(default=True)
  # Name of the function
  action = db.StringProperty(required=True)
  # Char sender, char and target must be in the same place
  char = db.ReferenceProperty(reference_class=Char, required=True, collection_name="actions_set")
  # Target of the action, char and target must be in the same place
  target = db.ReferenceProperty(collection_name="actions_targeted_set")
  # Args of the action
  args = JsonProperty(default=[])
  
  # timestamp is updated on create
  created = db.DateTimeProperty(auto_now_add=True)
  # timestamp is updated on every refresh
  last_modified = db.DateTimeProperty(auto_now=True)



def move(action, response):
  args = action.args
  
  #position = [args[0], args[1]]
  mx = args[0] - action.char.x
  my = args[1] - action.char.y
  
  # IT MUST BE CHECKED IN ACTION_HANDLER
  # o char esta onde quer ir
  #if mx == 0 and my == 0:
  #  action.active = False
  #  return
  
  if abs(mx)>abs(my):
    if mx>0:
      action.char.x += 1
    else:
      action.char.x -= 1
    add_response(response, 'objects', action.char, 'x', action.char.place)
  else:
    if my>0:
      action.char.y += 1
    else:
      action.char.y -= 1
    add_response(response, 'objects', action.char, 'y', action.char.place)
  
  # verifica se o char ja chegou onde queria
  if action.char.x == args[0] and action.char.y == args[1]:
    pass # action.active = False # JUST FOR DEBUG !!!
  
  
  

