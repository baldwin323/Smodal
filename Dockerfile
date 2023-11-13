# Dockerfile at the root of the repository
# This Dockerfile is updated to ensure that both the Django and React apps are built correctly
# It also makes sure all the necessary dependencies are installed and the correct commands are run

# Start with a base image containing Python where Django backend will be built
FROM python:3.8-alpine as backend

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the working directory within the Docker image
COPY ./backend .

# Update pip and install any necessary dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for the Django server
EXPOSE 8000

# Run the Django server when the Docker container has started.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Build the React frontend from Node.js image
FROM node:lts-alpine as frontend

# Set the working directory in the Docker container to /app
WORKDIR /app

# Copy the current directory contents (React app) into the container at /app
COPY ./frontend .

# Install any necessary dependencies
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run 'npm run build' for React's production build when the Docker container starts
RUN npm run build

# The final Docker image is created from the Nginx alpine base image to serve the React app and proxy the Django backend
FROM nginx:alpine

# Nginx will listen on this port
EXPOSE 80

# Copy the Django app from the intermediate Django image into the new Docker image at /app/backend
COPY --from=backend /app/ /app/backend

# Copy the built React static files from the intermediate Node.js image into the new Docker image at /var/www
COPY --from=frontend /app/build /var/www

# Copy the Nginx configuration file into the new Docker image to configure Nginx
COPY nginx.conf /etc/nginx/conf.d

# Run Nginx when the Docker container starts
CMD ["nginx", "-g", "daemon off;"]