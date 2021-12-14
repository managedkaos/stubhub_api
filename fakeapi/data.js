const faker = require("faker");
const fs = require("fs");
const generateEventsData = (number) => {
  const events = [];
  while (number >= 0) {
    events.push({
           id: number,
           status: faker.datatype.boolean(),
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
               latitude: faker.datatype.number(),
               longitude: faker.datatype.number()
           },
           timezone: faker.random.word(),
           currencyCode: faker.random.word(),
           ticketInfo: {
               minPrice: faker.datatype.number(),
               minListPrice: faker.datatype.number(),
               maxListPrice: faker.datatype.number(),
               totalTickets: faker.datatype.number(),
               totalListings: faker.datatype.number()
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
  JSON.stringify({ events: generateEventsData(100000) })
);
