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
# Install backend dependencies
RUN pip install -r requirements.txt
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
CMD ["nginx", "-g", "daemon off;"]

# Set environment variables for the app
ENV APP_ENV=kinsta 
ENV DB_HOST=database_kinsta_example
ENV DB_NAME=my_database_name 
ENV DB_USER=my_database_user 
ENV DB_PASS=my_database_password