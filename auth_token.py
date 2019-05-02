import base64
import ConfigParser

api = ConfigParser.ConfigParser()
api.read('stubhub-api.txt')

app_token = api.get('stubhub', 'application_token')
consumer_key = api.get('stubhub', 'consumer_key')
consumer_secret = api.get('stubhub', 'consumer_secret')

combo = consumer_key + ':' + consumer_secret

basic_authorization_token = base64.b64encode(combo)

print basic_authorization_token
