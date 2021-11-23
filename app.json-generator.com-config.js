JG.repeat(1, {
    "numFound": 1,
    "events": [
        {
  id: JG.integer(100000,500000),
    "status": "Active",
    "locale": "en_US",
    "name": JG.loremIpsum({units: 'words', count: 4}),
    "description": JG.loremIpsum({units: 'sentences', count: 4}),
    "webURI": "/event/123456789",
    "eventDateLocal": "2022-01-09T13:00:00-0500",
    "eventDateUTC": "2022-01-09T18:00:00+0000",
    "createdDate": "2021-04-20T04:30:12+0000",
    "lastUpdatedDate": "2021-08-21T19:42:01+0000",
    "hideEventDate": false,
    "hideEventTime": false,
        "venue": {
            "id": 448258,
            "city": "Atlanta",
            "name": "Mercedes-Benz Stadium",
            "state": "GA",
            "country": "US",
            "latitude": 33.75501,
            "longitude": -84.40186,
            "postalCode": "30313",
            "venueConfigId": 1243361,
            "venueConfigName": "Football - Falcons - Dynamic"
        },
    "timezone": "EST",
    "performers": [
        {
            "id": JG.integer(100000,500000),
            "name": "Atlanta Falcons"
        },
        {
            "id": JG.integer(100000,500000),
            "name": JG.loremIpsum({units: 'words', count: 2}),
            "role": "AWAY_TEAM"
        }
    ],
    "ancestors": {
        "categories": [
            {
                "id": JG.integer(100000,500000),
                "name": "Sports"
            },
            {
                "id": JG.integer(100000,500000),
                "name": "Football"
            }
        ],
        "groupings": [
            {
                "id": JG.integer(100000,500000),
                "name": "NFL"
            },
            {
                "id": JG.integer(100000,500000),
                "name": "Regular Season NFL"
            }
        ],
        "performers": [
            {
                "id": JG.integer(100000,500000),
                "name": "Atlanta Falcons"
            }
        ]
    },
    "categoriesCollection": {
        "categories": [
            {
                "id": JG.integer(100000,500000),
                "name": "Football"
            }
        ]
    },
    "currencyCode": "USD",
    "ticketInfo": {
        "minPrice": JG.floating(1,1000,2),
        "minListPrice": JG.floating(1,1000,2),
        "maxListPrice": JG.floating(1,1000,2),
        "totalTickets": JG.integer(),
        "totalListings": JG.integer()
    }
}]});
