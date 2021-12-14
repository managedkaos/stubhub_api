FROM node:alpine
WORKDIR /usr/app
RUN npm install faker && npm install -g json-server
COPY data.js /usr/app
RUN node /usr/app/data.js
EXPOSE 3004
CMD ["json-server", "--watch", "/usr/app/db.json", "--port=3004", "--host=0.0.0.0"]

