# Dockerfile at the root of the repository
# This Dockerfile is used to build both the Django and React apps, and configures Nginx

# Build the Django backend
FROM python:3.8-alpine as backend
WORKDIR /app
COPY ./backend .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Build the React frontend
FROM node:lts-alpine as frontend
WORKDIR /app
COPY ./frontend .
RUN npm install
RUN npm run build

# Final Nginx stage that serves the built React app and proxies to the Django backend
FROM nginx:alpine
EXPOSE 80
COPY --from=backend /app/ /app/backend
COPY --from=frontend /app/build /var/www
COPY nginx.conf /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]
