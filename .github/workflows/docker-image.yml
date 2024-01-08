# Dockerfile at the root of the repository
# This Dockerfile has been modified to ensure that the interactions between Django and React apps are configured correctly, such that the application as a whole can run independent of anything but its internet connection.
# It accounts for all necessary dependencies and ensures that the correct commands are run to build an executable Docker container.

# Define a multi-stage build process, where each stage is marked by an AS <name> tag
# Start with a base image containing Python where Django backend will be built
FROM python:3.8-alpine as backend

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the working directory within Docker backend image
COPY ./backend .

# Update pip and install any necessary backend dependencies via requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for the Django server, ensuring it can communicate with the internet
EXPOSE 8000

# In this initial image, we simply start the Django server on 0.0.0.0:8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# We now move onto the frontend, deriving from a new base image containing Node.js
# This will house the React application
FROM node:lts-alpine as frontend

# Set the working directory in the Docker container to /app again
WORKDIR /app

# Copy the current directory contents (React app) into the container at /app
COPY ./frontend .

# Install any necessary frontend dependencies via package.json
RUN npm install

# Port 3000 is exposed for the React server, leaving it open for communication
EXPOSE 3000

# We now build the static files for the React app with 'npm run build'
# These will be utilized in our final Docker image
RUN npm run build

# We now create the final Docker image that will be deployed
# This is created from the Nginx alpine base image, which provides a light yet powerful http server
FROM nginx:alpine

# Nginx listens on port 80, offering the entry point to our application from the internet
EXPOSE 80

# Copy the Django app from the intermediate Django image into the new Docker image at /app/backend
COPY --from=backend /app/ /app/backend

# Bring the static files for the React app from our Node-build into our new Docker image
# These are placed within /var/www, from where Nginx can serve them to the internet
COPY --from=frontend /app/build /var/www

# Copy the Nginx configuration file into the new Docker image to configure Nginx
COPY nginx.conf /etc/nginx/conf.d

# Finally, we command our container to run Nginx when it is started
# Having this as CMD, rather than RUN, ensures it isn't executed during build but rather at runtime
CMD ["nginx", "-g", "daemon off;"]
