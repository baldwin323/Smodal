# Dockerfile for smodal
# This Dockerfile describes the necessary steps to build the Docker image
FROM python:3.7-slim-buster

# Set a working directory
WORKDIR /app

# Copy everything in the current directory to our image
COPY . .

# Install requirements
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]

# End of Dockerfile
