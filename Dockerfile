```Dockerfile
# Python image to use as a base
FROM python:3.9-slim as builder

# Add Python to path and set python version
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.9"

# Setting the workdir to /builder
WORKDIR /builder

# Copying application requirements and source code to /builder
COPY requirements.txt /builder
COPY src /builder/src

# Install Python packages from requirements.txt without caching
RUN pip3 install --no-cache-dir -r requirements.txt

# Start new stage for the app 
FROM python:3.9-slim as app

# Add Python to path and set python version
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.9"

# Also install nginx and necessary tools for our Angular setup as part of our docker set-up
RUN apt-get update && apt-get install -y nginx curl gnupg

# Install NodeJS, which is required for Angular
RUN curl -sL https://deb.nodesource.com/setup_17.x | bash -
RUN apt-get install -y nodejs

# Install the Angular CLI, specifying version 17
RUN npm install -g @angular/cli@17

# Copying nginx config file
COPY nginx.conf /etc/nginx/nginx.conf

# Setting the workdir to /app
WORKDIR /app

# Copy Python packages from builder stage and application source code to the app stage
COPY --from=builder /builder/venv/lib/python3.9/site-packages /app/venv/lib/python3.9/site-packages
COPY --from=builder /builder/src /app

# Copy the application file to the current directory
COPY frontend.js .

# Changes for Kinsta environment
# Update Dockerfile to work in a Kinsta environment
ENV KINSTA_DEPLOYMENT='TRUE'

# Build the Angular application
# Using the Angular CLI installed globally via npm, create a production build of the Angular application
RUN ng build --prod

# Expose the nginx server port
EXPOSE 80

# The command that will be run on container start
CMD ["node", "frontend.js"]
```
