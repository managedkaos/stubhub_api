import json
import time
import requests
import ConfigParser

# read the configurations
api = ConfigParser.ConfigParser()
api.read('stubhub-api.txt')

# set up the headers that are common for each request
headers = {
    'authorization': "Bearer " + api.get('stubhub', 'application_token'),
    'accept': "application/json",
    }

# for each event ID from the config file...
for event_id in json.loads(api.get("ids","event_ids")):
    # get the data from stubhub for the event and the event's inventory
    querystring = {"eventId":str(event_id),"sectionStats":"true","zoneStats":"true", "rows":"9999"}
    event_response = requests.request("GET", api.get("stubhub","event_url") + str(event_id), headers=headers)
    inventory_response = requests.request("GET", api.get("stubhub","inventory_url"), headers=headers, params=querystring)

    # save the response as json
    event = event_response.json()
    inventory = inventory_response.json()

    # print the event summary
    print event['title']
    print "\tTotal Listings : " + str(inventory['pricingSummary']['totalListings'])
    print "\tMinimum Price  : $" + str(format(inventory['pricingSummary']['minTicketPrice'],'.2f'))
    print "\tMaximum Price  : $" + str(format(inventory['pricingSummary']['maxTicketPrice'],'.2f'))
    print "\tAverage Price  : $" + str(format(inventory['pricingSummary']['averageTicketPrice'],'.2f'))
    print

    # print a summary for each listing in the inventory
    print "listingId; currentPrice; listingPrice; row; quantity; sectionName; seatNumbers"

    for listing in inventory['listing']:
        print "%s; %s; %s; %s; %s; %s; %s" % (listing['listingId'], listing['currentPrice']['amount'], listing['listingPrice']['amount'], listing['row'], listing['quantity'], listing['sectionName'], listing['seatNumbers'])

    # delay each round to stay within the request limit (10 requests/minute)
    time.sleep(10)