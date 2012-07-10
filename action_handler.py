# action_handler.py
#
# will be called by /action

import datetime

from clients import get_client
from actions import actions_signatures
from actions import Action

from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api.channel import create_channel
from google.appengine.ext.webapp.util import run_wsgi_app

# Recives a signature of an action
# and check the args recived if it can execute the action.
def validate_args(signature_args, args):
  len_signature_args = len(signature_args)
  len_args = len(args)
  
  if len_signature_args != len_args:
    return False
  
  for i in range(len_signature_args):
    #response['errors'].append('s_ar['+str(i)+']:'+str(signature_args[i]))
    if signature_args[i] == str:
      try:
        args[i] = str(args[i])
      except:
        return False
    
    elif signature_args[i] == int:
      try:
        args[i] = int(args[i])
      except:
        return False
    
    elif signature_args[i] == float:
      try:
        args[i] = float(args[i])
      except:
        return False
  #response['errors'].append('FIM VALIDATE')
  return True



class ActionHandler(webapp.RequestHandler):
  """ CHANGED."""

  def get(self):
    # It can't be called by GET method.
    #self.redirect('/', permanent=True)
    # BUT FOR TEST...
    self.response.out.write(self.post())
  
  def post(self):
    user = users.get_current_user()
    if not user:
      self.error(403) # access denied
      return
    
    client = get_client(user)
    if not client:
      self.error(403) # access denied
      return
    
    #debug = self.request.get('debug', False)
    
    
    # CAUTION: IT WANNA BE BY ANOTHER WAY (NEED TO IMPLEMENT)
    #char.logged = True
    #char.put()
    
    #self.response.headers.add_header("Content-Type", 'application/json')
    
    # Action to execute
    action = self.request.get('action')
    
    # Arguments of the action
    args = self.request.get_all('args[]')
    # REMOVE ALL EMPTY VALUE OF THE ARGS
    for i in range(args.count('')):
      args.remove('')
    
    
    # Target of the action
    target_id = self.request.get('target')
    if target_id:
      target = db.get(db.Key(target_id))
      # DEBUG
      if not target:
        response['alert'].append('TARGET NOT AVAILABLE')
    else:
      target = None
    
    
    # Client time that executed the action
    client_time = self.request.get('time')
    
    # Append to the response the action feedback or one alert or error if it has
    response = {
                  'action': action,
                  'target': target,
                  'args': args,
                  'client_time': client_time,
                  #'server_hour': datetime.datetime.now().strftime('%I:%M:%S'),
                  'self': client.char.id,
                  #'object': {}, Thinking about it here in action_handler
                  #'listener': {}, Not implemented yet
                  'alert': [],
                  'error': [],
                }
    
    
    if action == 'ping':
      pass
    
    elif action == 'get_channel_token':
      client.channel_token = create_channel(client.id)
      client.put()
      response['channel_token'] = client.channel_token
    
    elif action in actions_signatures:
      #response['alert'].append('Action found:' + action)
      if validate_args(actions_signatures[action], args):
        #function = getattr(actions, action)
        #function(client, response, args)
        query = db.Query(Action)
        query.filter('active =', True)
        query.filter('action =', action)
        query.filter('char =', client.char)
        saved_action = query.get()
        if saved_action:
          response['alert'].append('ACTION ACTIVE FOUND')
          saved_action.args = args
          saved_action.target = target
          saved_action.put()
        else:
          response['alert'].append('NEW ACTION CREATED')
          action = Action(char=client.char,
                          action=action,
                          args=args,
                          target=target)
          action.put()
          
        
      else:
        response['error'].append('ERROR TO VALIDATE ARGS')
    
    else:
      response['error'].append('ACTION NOT ALLOWED')
    
    self.response.out.write(simplejson.dumps(response))
    return
    

# --------------------------------------------------------------------- #
application = webapp.WSGIApplication(
    [
      ('/.*', ActionHandler)
    ],
    debug = True
  )

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
