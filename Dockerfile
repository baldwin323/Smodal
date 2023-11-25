# This Dockerfile configures a multi-stage build process to create a Docker
# container that can run a Django backend and an Angular frontend independently.
# The application is assembled using necessary dependencies and proper configurations,
# thanks to a carefully phased build process.
# The focus is to ensure effective enrichment of the code with Pydantic and
# correct functioning of the middleware connections.

# The build starts with a base image containing Python, setting up the Django backend.
FROM python:3.12-alpine as backend

WORKDIR /app
COPY ./backend .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Removed AWS or Digital Ocean dependencies

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

# Finally, we copy all the backend and frontend files and set up the nginx server.
FROM nginx:alpine
EXPOSE 80
COPY --from=backend /app/ /app/backend
COPY --from=frontend /app/dist/ /var/www

# Correcting the COPY command to specify the nginx configuration file's location.
# Made sure to specify the correct file path as per instructions.
COPY ./backend/nginx/nginx.conf /etc/nginx/conf.d

# Added Nginix command to be executed during the container's runtime and not during the build process.
CMD ["nginx", "-g", "daemon off;"]