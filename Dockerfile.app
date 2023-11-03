```Dockerfile
# Stage 1: Node.js build
FROM node:14 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Python server
FROM python:3.8
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy built static files from build stage
COPY --from=build /app/build /app/static 

# Copy the rest of the code
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
This Dockerfile first creates a Node.js environment to build the frontend and then sets up the Python environment to run the server. It installs dependencies from the package.json file for Node.js and from the requirements.txt file for Python. Next, it copies the built frontend files from the build stage to a static directory in the Python environment. Finally, it exposes port 8000 and starts the server.