# This Dockerfile configures a multi-stage build process to create a Docker container that can run a Django backend and React frontend independently.
# The application is assembled with necessary dependencies and proper configurations, thanks to a carefully phased build process.

# The build process is initiated from a base image containing Python 3.8, setting up the Django backend.
FROM python:3.8-alpine as backend

# Defining the work directory in Docker as /app
WORKDIR /app

# Copy the current directory contents into /app in Docker
COPY ./backend .

# Update pip to its latest version and install backend dependencies using requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Django is set to run on port 8000; therefore, it's exposed to the network.
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Moving onto creating the frontend with Node.js base image. 
FROM node:lts-alpine as frontend

# The work directory in Docker is set again to /app
WORKDIR /app

# Bring in the contents of the directory into /app within Docker
COPY ./frontend .

# Install necessary frontend dependencies using package.json
RUN npm install

# The React server will run on port 3000, so the port is exposed.
EXPOSE 3000
RUN npm run build

# Finally, create the deployable Docker image. 
# This configuration uses Nginx:alpine base image to ensure a light but robust HTTP server for the final product.
FROM nginx:alpine

# Nginx listens on port 80, creating a gateway for our application to the network.
EXPOSE 80

# Copy the Django app from the working directory into /app/backend in our Docker image.
COPY --from=backend /app/ /app/backend

# Transfer static files for the React app (from Node-build) into /var/www for Nginx to serve.
COPY --from=frontend /app/build /var/www

# Bring in the Nginx configuration file into Docker to setup Nginx.
COPY nginx.conf /etc/nginx/conf.d

# Use CMD instead of RUN to make sure Nginx runs at the container's runtime, not during the build process.
CMD ["nginx", "-g", "daemon off;"]