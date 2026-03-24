FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose Vite dev port
EXPOSE 3000

# Run Vite with --host so it is accessible from outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
