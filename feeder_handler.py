# feeder_handler.py
#
# /feeder
#
# This feeder will feed the clients, and they will update their screens

import datetime
from time import sleep

from clients import get_client
from updates import Update
from chars import Char
from items import Item
from updates import Update
from aux import add_response
from aux import is_development

from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api.channel import send_message
from google.appengine.ext.webapp.util import run_wsgi_app




def full_updates(client):
  
  objects = {}
  query = db.Query(Char)
  query.filter('active =', True)
  query.filter('online =', True)
  query.filter('place =', client.char.place)
  for char in query:
    objects[char.id] = char.get_attrs()
  
  query = db.Query(Item)
  query.filter('active =', True)
  query.filter('place =', client.char.place)
  for item in query:
    objects[item.id] = item.get_attrs()
  
  
  return {
              'self': client.id,
              #'server_last_update': memcache.get('server_last_update'),
              #'server_delay': memcache.get('server_delay'),
              'place': client.char.place.get_attrs(),
              'objects': objects,
            }
    
    
    

class FeederHandler(webapp.RequestHandler):
  """ Feeder
      waiting for time to write """
  def get(self):
    return self.post(is_get=True)
  def post(self, is_get=False):
  
    if is_get:
      self.response.out.write('is_get = '+str(is_get)+'<br />')
    
    user = users.get_current_user()
    if not user:
      self.error(403) # access denied
      return
    
    client = get_client(user)
    if not client:
      self.error(403) # access denied
      return
    
    
    
    if is_development or is_get:
      loop_range = 1
    else:
      loop_range = 28
    for i in range(loop_range):
      
      
      # Checks if the player d made the atualization in this second
      # if he made the atualization this second,
      # he must wait to the next second
      # Server delay is a timedelta that the server
      # spent to process last update, something like 3500microseconds
      
      feeder_start = datetime.datetime.now()
      deltatime = feeder_start - client.last_update
      if deltatime.seconds == 0:
        # now is less than a second since the last update
        
        # Estimated time to sleep
        sleep_time = float(1000000 - deltatime.microseconds)/1000000
        if is_development or is_get:
          self.response.out.write('sleep: '+str(sleep_time)+'<br />')
        sleep(sleep_time)
        feeder_start = datetime.datetime.now()
      
      
      # This is a especial case that the client has just opened the browser
      # and he needs to get full_updates of all places
      if client.last_update == datetime.datetime.min:
        if is_development or is_get:
          self.response.out.write('FULL UPDATES<br />')
        updates = full_updates(client)
      
      
      else:
        """
        # Henceforward (daqui em diante) assume that the char have ur screen
        
        # If the server has not responded yet, wait for its response
        server_last_update = memcache.get('server_last_update')
        if not server_last_update:
          # We can't set datetime.datetime.min,
          # because strftime can't mannage years before 1900
          server_last_update = datetime.datetime(2000,1,1)
        deltatime = feeder_start - server_last_update
        while deltatime.seconds > 0:
          # Server do not atualize in this second, wait the atualization
          sleep(float(server_delay*(10))/1000000)
          server_last_update = memcache.get('server_last_update')
          if not server_last_update:
            # We can't set datetime.datetime.min,
            # because strftime can't mannage years before 1900
            server_last_update = datetime.datetime(2000,1,1)
          deltatime = feeder_start - server_last_update
          if datetime.datetime.now().second > feeder_start.second:
            # It tryed all this second for te actualization
            break
        """
        updates = {
                    #'server_hour':server_last_update.strftime('%I:%M:%S ')
                    #              + ':' +str(server_last_update.microsecond),
                    #'server_delay':server_delay
                  }
        
        
        if is_development or is_get:
          self.response.out.write('HALF UPDATES<br />')
        
        
        query = db.Query(Update)
        query.filter('place =', client.char.place)
        query.filter('datetime >', client.last_update)
        for update in query:
          new_update = update.update
          if is_development or is_get:
            self.response.out.write('update:'+str(update.place)+'<br />')
          
          # ADDING UPDATES CHANGES
          for update_type in new_update:
            if type(new_update[update_type]) == str:
              updates[update_type] = new_update[update_type]
            
            elif type(new_update[update_type]) == list:
              if not update_type in updates:
                updates[update_type] = []
              for new_obj in new_update[update_type]:
                updates[update_type].append(new_obj)
            
            elif type(new_update[update_type]) == dict:
              if not update_type in updates:
                updates[update_type] = {}
              for key in new_update[update_type]:
                updates[update_type][key] = new_update[update_type][key]
          
      
    
    
    
      client.last_update = feeder_start
      
      #updates = 'testando'
      if updates:
        #updates['object'] = object_list
        if is_development or is_get:
          self.response.out.write('sending to:'+client.id+'<br />')
          self.response.out.write('<br />'+simplejson.dumps(updates)+'<br />')
        send_message(client.id, simplejson.dumps(updates))
      else:
        self.response.out.write('no updates to send to:'+client.channel_token+'<br />')
      
    client.put()
      
    
# ----------------------------------------------------------------------- #
application = webapp.WSGIApplication(
    [
      ('/.*', FeederHandler)
    ],
    debug = True
  )

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
