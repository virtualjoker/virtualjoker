# jsonproperty.py
#
# property: JsonProperty

from django.utils import simplejson
from google.appengine.ext import db

class JsonProperty(db.TextProperty):
	data_type = 'json'
    
	# I don't like to implements it
	def validate(self, value):
		return value
    
	def get_value_for_datastore(self, model_instance):
		result = super(JsonProperty, self).get_value_for_datastore(model_instance)
		result = simplejson.dumps(result)
		return db.Text(result)

	def make_value_from_datastore(self, value):
		try:
			value = simplejson.loads(str(value))
		except:
			pass

		return super(JsonProperty, self).make_value_from_datastore(value)

