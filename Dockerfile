# The code is improved from the original Dockerfile where comments are added for each step, 
# unnecessary files are not copied, multi-stage build is used to reduce the size of the final image.

# Dockerfile for smodal
# This Dockerfile describes the necessary steps to build the Docker image

# 'builder' stage—this is a temporary image used for building our application
FROM python:3.7-slim-buster as builder

# Set a working directory for the 'builder' stage
WORKDIR /builder

# Copy only the necessary files for the 'builder' stage
# This includes the Python requirements file and the source code
COPY requirements.txt /builder
COPY src /builder/src

# Install requirements in the 'builder' stage
# We separate this command because Docker can cache the output to speed up rebuilds
RUN pip install -r requirements.txt


# 'app' stage—this contains the final application image
FROM python:3.7-slim-buster as app

# Set a working directory for the 'app' stage
WORKDIR /app

# Copy the necessary files from the 'builder' stage to the 'app' stage
# This includes any installed Python packages and the compiled application code
COPY --from=builder /builder /app

# Expose the port where the app is running
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]

# End of Dockerfile