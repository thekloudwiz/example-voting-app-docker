FROM node:18-slim

WORKDIR /app

# Install nodemon globally
RUN npm install -g nodemon

# Install dependencies
COPY package.json /app/package.json
RUN npm install

# Move node_modules to avoid volume override
RUN mv /app/node_modules /node_modules

# Copy application code
COPY . /app

ENV PORT 80
EXPOSE 80

CMD ["node", "server.js"]