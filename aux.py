# aux.py

import os


is_development = os.environ['SERVER_SOFTWARE'].startswith('Development')


def add_response(response, where, object_id, atribute, value):
  response[where][object_id][atribute] = value
  
