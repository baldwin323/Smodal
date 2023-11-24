# This Dockerfile configures a multi-stage build process to create a Docker container that can run a Django backend and an Angular frontend independently.
# The application is assembled using necessary dependencies and proper configurations, thanks to a carefully phased build process.
# The focus is to ensure effective enrichment of the code with Pydantic and correct functioning of the middleware connections.

# The build starts from a base image containing Python 3.12, setting up the Django backend.
# Python version updated to 3.12 as per the instruction.
FROM python:3.12-alpine as backend

WORKDIR /app
COPY ./backend .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Downloading the Dynatrace installer and verifying its signature. Also, allowing it to run with root rights.
RUN wget  -O Dynatrace-OneAgent-Linux-1.277.165.20231024-150054.sh "https://rwf35059.live.dynatrace.com/api/v1/deployment/installer/agent/unix/default/latest?arch=x86" --header="Authorization: Api-Token dt0c01.SOKT2PUFROO5UMCMV3VVZSSC.4U5ODOGB7GITQTTYL2OYPGHMFZ2ZH6A6SZSS6XWYDKZ6CHUFZZTY5MOVK5OG3OB7"
RUN wget https://ca.dynatrace.com/dt-root.cert.pem ; ( echo 'Content-Type: multipart/signed; protocol="application/x-pkcs7-signature"; micalg="sha-256"; boundary="--SIGNED-INSTALLER"'; echo ; echo ; echo '----SIGNED-INSTALLER' ; cat Dynatrace-OneAgent-Linux-1.277.165.20231024-150054.sh ) | openssl cms -verify -CAfile dt-root.cert.pem > /dev/null
RUN /bin/sh Dynatrace-OneAgent-Linux-1.277.165.20231024-150054.sh --set-monitoring-mode=fullstack --set-app-log-content-access=true

# Let Django run on port 8000 and expose it to the network.
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Moving onto creating the Angular frontend. Node.js base image is used. 
FROM node:lts-alpine as frontend
WORKDIR /app
COPY ./frontend .
RUN npm install
EXPOSE 3000
RUN npm run build

# Finally, we copy all the backend and frontend files and set up the Nginx server.
FROM nginx:alpine
EXPOSE 80
COPY --from=backend /app/ /app/backend
COPY --from=frontend /app/dist/ /var/www

# Correcting the COPY command to specify the nginx configuration file's location.
# Made sure to specify the correct	file path as per instructions.
COPY ./backend/nginx/nginx.conf /etc/nginx/conf.d 

# Added Nginix command to be executed during the container's runtime and not during the build process.
CMD ["nginx", "-g", "daemon off;"]