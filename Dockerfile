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
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Stage 3: Build Nginx server
FROM nginx:alpine
EXPOSE 80
COPY --from=frontend /app/dist/ /var/www
COPY --from=backend /app/ /app/backend
COPY ./backend/nginx/nginx.conf /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]

# Set environment variables for the app
ENV APP_ENV=kinsta 
ENV DB_HOST=database_kinsta_example
ENV DB_NAME=my_database_name 
ENV DB_USER=my_database_user 
ENV DB_PASS=my_database_password
