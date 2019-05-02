import requests
import ConfigParser

api = ConfigParser.ConfigParser()
api.read('stubhub-api.txt')

headers = {
    'authorization': "Bearer " + api.get('stubhub', 'application_token'),
    'accept': "application/json",
    }

querystring = {"eventId":"9566731","sectionStats":"true","zoneStats":"true", "rows":"9999"}

response = requests.request("GET", api.get("stubhub","inventory_url"), headers=headers, params=querystring)

print(response.text)