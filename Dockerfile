# Dockerfile for Smodal - resolved conflicts

# Stage 1: Build Angular frontend
FROM node:lts-alpine as frontend
WORKDIR /app
COPY . .
RUN npm install
RUN ng build --prod

# Stage 2: Build Django backend
FROM python:3.12-alpine as backend
WORKDIR /app
COPY ./backend .

# Install backend dependencies and Docker
RUN apk add --no-cache docker \
    && pip install -r requirements.txt

# Django uses port 8000 for its server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Stage 3: Build Nginx server
FROM nginx:alpine

# Nginx serves the application on port 80
EXPOSE 80
COPY --from=frontend /app/dist/ /var/www
COPY --from=backend /app/ /app/backend

# Configure Nginx with our settings
COPY ./backend/nginx/nginx.conf /etc/nginx/conf.d

# Start Nginx in background - no changes
CMD ["nginx", "-g", "daemon off;"]

# Added an additional Nginx configuration to handle 503 error by directing it to a custom error page or fallback service
# in case of the main service unavailability. - no changes
COPY ./backend/nginx/error503.conf /etc/nginx/conf.d

# Set environment variables for the app
# These variables are specific to the Kinsta deployment
ENV APP_ENV=kinsta 
ENV DB_HOST=database_kinsta_example
ENV DB_NAME=my_database_name 
ENV DB_USER=my_database_user 
ENV DB_PASS=my_database_password

# API key for Smodal-Kinsta-app - no changes
ENV SMODAL_API_KEY=8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0

# Correct the npm configuration error message by setting NODE_ENV to 'production' 
# to omit dev dependencies from the final docker image - no changes
ENV NODE_ENV=production