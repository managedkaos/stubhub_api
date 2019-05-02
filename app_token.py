import base64
import requests
import ConfigParser

api = ConfigParser.ConfigParser()
api.read('stubhub-api.txt')

app_token = api.get('stubhub', 'application_token')
consumer_key = api.get('stubhub', 'consumer_key')
consumer_secret = api.get('stubhub', 'consumer_secret')

stubhub_username = api.get('stubhub', 'username')
stubhub_password = api.get('stubhub', 'password')

combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo)

payload = "grant_type=password&username="+stubhub_username+"&password="+stubhub_password+"&scope=Production"
headers = {
    'authorization': "Basic " + basic_authorization_token,
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", api.get("stubhub","login_url"), data=payload, headers=headers)

print(response.text)
