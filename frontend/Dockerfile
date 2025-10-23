# Use official Node.js image
FROM node:18-bullseye-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install all dependencies (including dev)
RUN npm install

# Copy rest of the project
COPY . .

# Expose Render’s default web port
EXPOSE 3000

# Set environment variable
ENV NODE_ENV=development
ENV PORT=3000

# Start the Next.js app
CMD ["npm", "run", "dev"]
