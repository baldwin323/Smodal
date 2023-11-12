# Dockerfile at the root of the repository
# This Dockerfile is used to build both the Django and React apps, and configures Nginx

# Define the python version from which Django backend will be built
FROM python:3.8-alpine as backend
# Define the working directory in the Docker image
WORKDIR /app
# Copy Django application along with requirements file into image
COPY ./backend .
# Install the Django requirements
RUN pip install -r requirements.txt
# Indicate the port number the container should expose
EXPOSE 8000
# Run the Django server on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Build the React frontend from Node.js image
FROM node:lts-alpine as frontend
# Create a directory named app in the Docker image
WORKDIR /app
# Copy the React app into the Docker image
COPY ./frontend .
# Install the Node.js dependencies
RUN npm install
# Build the static files for the React app
RUN npm run build

# Configure the Nginx server to serve the built React app and proxy the Django backend
# Create the final Docker image from the Nginx alpine base image
FROM nginx:alpine
# Nginx listens on this port
EXPOSE 80
# Copy the Django app from the intermediate Django image
COPY --from=backend /app/ /app/backend
# Copy the built React app from the intermediate Node.js image
COPY --from=frontend /app/build /var/www
# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d
# Start the Nginx server on the container startup
CMD ["nginx", "-g", "daemon off;"]