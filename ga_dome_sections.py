import json
import requests
import ConfigParser

sections = []

api = ConfigParser.ConfigParser()
api.read('stubhub-api.txt')

headers = {
    'authorization': "Bearer " + api.get('stubhub', 'application_token'),
    'accept': "application/json",
    }

querystring = {"eventId":"9566731","sectionStats":"true","zoneStats":"true"}

response = requests.request("GET", api.get("stubhub","inventory_url"), headers=headers, params=querystring)

data = response.json()

print "Section ID\tSection Name"
for section in data['section_stats']:
    print str(section['sectionId']) + "\t" + section['sectionName']
