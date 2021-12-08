FROM node:alpine
WORKDIR /usr/app
COPY . /usr/app
RUN npm install faker && npm install -g json-server
RUN node /usr/app/data.js
RUN cat /usr/app/db.json
EXPOSE 3004
CMD ["json-server", "--watch", "/usr/app/db.json", "--port=3004", "--host=0.0.0.0"]

