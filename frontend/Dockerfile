# Simple Python HTTP server for QuantumTrade frontend
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the built frontend files
COPY dist/ /app/dist/

# Expose port
EXPOSE 5173

# Serve the application using Python's built-in HTTP server
CMD ["python", "-m", "http.server", "5173", "--directory", "dist"]

# Simple static file server for QuantumTrade frontend
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Install Supabase client
RUN npm install @supabase/supabase-js

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Install a simple HTTP server
RUN npm install -g serve

# Serve the application
CMD ["serve", "-s", "dist", "-l", "5173"]