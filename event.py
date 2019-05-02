import requests
import ConfigParser

api = ConfigParser.ConfigParser()
api.read('stubhub-api.txt')

headers = {
    'authorization': "Bearer " + api.get('stubhub', 'application_token'),
    'accept': "application/json",
    }

response = requests.request("GET", api.get("stubhub","event_url")+"9566731", headers=headers)

print(response.text)
