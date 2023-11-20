# This Dockerfile configures a multi-stage build process to create a Docker container that can run a Django backend and React frontend independently.
# The application is assembled with necessary dependencies and proper configurations, thanks to a carefully phased build process.

# The build process is initiated from a base image containing Python 3.8, setting up the Django backend.
# Updated python version to 3.12 as per the instruction  
FROM python:3.12-alpine as backend

# Defining the work directory in Docker as /app
WORKDIR /app

# Copy the current directory contents into /app in Docker
COPY ./backend .

# Update pip to its latest version and install backend dependencies using requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Downloading the Dynatrace installer
RUN wget  -O Dynatrace-OneAgent-Linux-1.277.165.20231024-150054.sh "https://rwf35059.live.dynatrace.com/api/v1/deployment/installer/agent/unix/default/latest?arch=x86" --header="Authorization: Api-Token dt0c01.SOKT2PUFROO5UMCMV3VVZSSC.4U5ODOGB7GITQTTYL2OYPGHMFZ2ZH6A6SZSS6XWYDKZ6CHUFZZTY5MOVK5OG3OB7"

# Verify signature
RUN wget https://ca.dynatrace.com/dt-root.cert.pem ; ( echo 'Content-Type: multipart/signed; protocol="application/x-pkcs7-signature"; micalg="sha-256"; boundary="--SIGNED-INSTALLER"'; echo ; echo ; echo '----SIGNED-INSTALLER' ; cat Dynatrace-OneAgent-Linux-1.277.165.20231024-150054.sh ) | openssl cms -verify -CAfile dt-root.cert.pem > /dev/null

# Run the installer with root rights
RUN /bin/sh Dynatrace-OneAgent-Linux-1.277.165.20231024-150054.sh --set-monitoring-mode=fullstack --set-app-log-content-access=true

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

# Make sure the nginx.conf file is specified in its appropriate location in the repository.
COPY ./nginx/nginx.conf /etc/nginx/conf.d
# Used ./nginx/ to specify the location, replace with the actual directory where the nginx.conf file is placed.

# Use CMD instead of RUN to make sure Nginx runs at the container's runtime, not during the build process.
CMD ["nginx", "-g", "daemon off;"]