# feeder_handler.py
#actior
# /feeder
#
# This feeder will feed the clients, and they will update their screens

import datetime
from time import sleep
from time import time

from clients import get_client
from actions import Action
from updates import Update
from aux import is_development
import actions
#from maps import Map
from chars import Char
#from items import Item

from django.utils import simplejson
from google.appengine.ext import db
#from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api.channel import send_message
from google.appengine.ext.webapp.util import run_wsgi_app




class ServerHandler(webapp.RequestHandler):
  """ ServerHandler
      This ServerHandler will be called by a task queue,
      this task will be enqueued by cron_jobs in constant time """
  def get(self):
    
    debug = self.request.get('debug', False)
    
    
    server_current = datetime.datetime.now()
    memcache.set('server_current', server_current)
    
    # Wait for the previous server to finish its update
    #server_delay = memcache.get('server_delay')
    #if server_delay:
    #  sleep((float(server_delay)/1000000)*10)
      
    
    server_last_update = memcache.get('server_last_update')
    if not server_last_update:
      server_last_update = datetime.datetime.min
    
    # DEBUG
    if is_development or debug:
      self.response.out.write('is_development:  '+str(is_development)+'<br />')
      self.response.out.write('debug:  '+str(debug)+'<br />')
      self.response.out.write('server_current:  '+str(server_current)+'<br />')
      self.response.out.write('server_last_update: '+str(server_last_update)+'<br />')
    
    # Runs while the next instance opens and overrides the server_current
    # *** FAILS: If cache fails and returns None?
    #while server_current == memcache.get('server_current'):
    
    objects = memcache.get('objects')
    if not objects:
      objects = {}
      for i in range(500):
        objects[i] = Char(x=10, y=20)
    memcache.set('objects', objects)
    
    
    for i in range(60): 
      server_start = datetime.datetime.now()
      deltatime = server_start - server_last_update
      if deltatime.seconds == 0:
        
        sleep_next_s = float(1000000 - deltatime.microseconds)/1000000
        
        # DEBUG
        if is_development or debug:
          self.response.out.write('sleep: '+str(sleep_next_s)+'<br />')
        sleep(sleep_next_s)
        
        # Server sleeped and need to pick up server_start datetime again
        server_start = datetime.datetime.now()
      
      t0 = time()
      objects = memcache.get('objects')
      for id in objects:
        objects[id].x = 10
        objects[id].y = 20
      memcache.set('objects', objects)
      if is_development or debug:
        self.response.out.write('delay: '+
                                str(time() - t0)+
                                '<br />')
      
      """
      # HERE THE SERVER STARTS TO GENERATE THE UPDATE
      # this update will be update['place'] = {'objects':..., 'alert':....}
      update = {}
      query = db.Query(Action)
      query.filter('active =', True)
      all_actions = query.fetch(1000)
      all_objects = {}
      
      for action in all_actions:
        # Get the objects in all_objects if it was there
        if action.char.key() in all_objects:
          action.char = all_objects[action.char.key()]
        if action.target:
          if action.target.key() in all_objects:
            action.target = all_objects[action.target.key()]
        
        # Executes the action
        function = getattr(actions, action.action)
        # !!! BETTER PASS HERE JUST THE update[action.target.place]
        # !!! AND FIX THAT THE USER JUST CAN DO ACTIONS IN TARGETS PLACE
        # !!! AND TO MOVE AN OBJECT TO ANOTHER PLACE JUST DOING 2 ACTIONS
        function(action, update)
        
        # Put the objects in the all_objects to be saved after it
        all_objects[action.char.key()] = action.char
        if action.target:
          all_objects[action.target.key()] = action.target
      
      
      
      all_updates = []
      for place_key in update:
        all_updates.append(Update(
                                    place=place_key,
                                    update=update[place_key]
                                  ))
        
        if is_development or debug:
          self.response.out.write('update['+str(place_key)+']: '+
                                  str(server_last_update)+'<br />')
      
      
      db.put(all_updates)
      
      db.put(all_actions)
      # all_objects is a dict: all_objects[object.id] = object
      db.put(all_objects.values())
      
      server_last_update = server_start
      server_finish = datetime.datetime.now()
      server_delay = server_finish - server_start
      memcache.set('server_last_update', server_last_update)
      memcache.set('server_delay', server_delay.microseconds)
      """
      
      server_last_update = server_start
      #memcache.set('server_last_update', server_last_update)
      # DEBUG
      if is_development or debug:
        self.response.out.write('server_last_update: '+
                                str(server_last_update)+
                                '<br />')
        #self.response.out.write('server_delay: '+
        #                        str(server_delay.microseconds)+
        #                        '<br />')
      
      if is_development or debug:
        # IF is_development OR debug IT WILL RUNS JUST ONE TIME
        break
      
    
# ----------------------------------------------------------------------- #
application = webapp.WSGIApplication(
    [
      ('/.*', ServerHandler)
    ],
    debug = True
  )

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
