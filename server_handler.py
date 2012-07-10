# feeder_handler.py
#actior
# /feeder
#
# This feeder will feed the clients, and they will update their screens

import logging
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

def out(self, text, var = False):
  if not var:
    self.response.out.write(text + '<br/>')
  else:
    self.response.out.write(text + ': ' + str(var) + '<br/>')


class ServerHandler(webapp.RequestHandler):
  """ ServerHandler
      This ServerHandler will be called by a task queue,
      this task will be enqueued by cron_jobs in constant time """
  def get(self):
    
    debug = self.request.get('debug', False)
    
    action = self.request.get('action')
    out(self, 'action', action)
    
    server_last_update = datetime.datetime.min
    
    if action == 'populate_datastore':
      t0 = time()
      chars = []
      for i in range(500):
        chars.append(Char(x=10, y=20))
      db.put(chars)
      out(self, 'Chars created and saved in datastore', time()-t0)
      return
    
    if action == 'populate_memcache':
      t0 = time()
      objects = memcache.get('objects')
      if not objects:
        objects = {}
        for i in range(500):
          objects[i] = Char(x=10, y=20)
      memcache.set('objects', objects)
      out(self, 'Chars created and saved in cache', time()-t0)
      return
    
    for i in range(300): 
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
      
      
      if action == 'memcache':
        t0 = time()
        objects = memcache.get('objects')
        for id in objects:
          objects[id].x = 10
          objects[id].y = 20
        memcache.set('objects', objects)
        if is_development or debug:
          out(self, 'delay', time() - t0)
      
      
      if action == 'datastore':
        t0 = time()
        query = db.Query(Char)
        chars = query.fetch(500)
        for char in chars:
          char.x = 10
          char.y = 20
        db.put(chars)
        if is_development or debug:
          out(self, 'delay', time() - t0)
      
      server_last_update = server_start
      if is_development or debug:
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
