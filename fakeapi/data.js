const faker = require("faker");
const fs = require("fs");
const generateEventsData = (number) => {
  const events = [];
  while (number >= 0) {
    events.push({
           id: 100+number,
           status: faker.random.boolean(),
           locale: faker.random.locale(),
           name: faker.random.word(),
           description: faker.lorem.paragraph(),
           webURI: "http://google.com",
           eventDateLocal: faker.random.word(),
           eventDateUTC: faker.random.word(),
           createdDate: faker.random.word(),
           lastUpdatedDate: faker.random.word(),
           hideEventDate: faker.random.word(),
           hideEventTime: faker.random.word(),
           venue: {
               id: faker.random.word(),
               name: faker.random.word(),
               city: faker.random.word(),
               state: faker.random.word(),
               postalCode: faker.random.word(),
               country: faker.random.word(),
               venueConfigId: faker.random.word(),
               venueConfigName: faker.random.word(),
               latitude: faker.random.number(),
               longitude: faker.random.number()
           },
           timezone: faker.random.word(),
           currencyCode: faker.random.word(),
           ticketInfo: {
               minPrice: faker.random.number(),
               minListPrice: faker.random.number(),
               maxListPrice: faker.random.number(),
               totalTickets: faker.random.number(),
               totalListings: faker.random.number()
           },
           performers: faker.random.word(),
           ancestors: faker.random.word(),
           categoriesCollection: faker.random.word(),
           ingestionDate: Date.now()
    });
    number--;
  }
  return events;
};
fs.writeFileSync(
  "./db.json",
  JSON.stringify({ events: generateEventsData(10) })
);
