# Dockerfile for smodal
# This Dockerfile describes the necessary steps to build the Docker image

# 'builder' stage—this is a temporary image used for building our application
# Updated Python version to 3.12
FROM python:3.12-slim as builder

# Setting the environment path for Python 3.12
ENV PATH="/opt/python/bin:${PATH}"
ENV PYTHON="/opt/python/bin/python3.12"

# Set a working directory for the 'builder' stage
WORKDIR /builder

# Copy only the necessary files for the 'builder' stage
# This includes the Python requirements file and the source code
COPY requirements.txt /builder
COPY src /builder/src

# Install requirements in the 'builder' stage
# We separate this command because Docker can cache the output to speed up rebuilds
# Using pip3.12 with respect to Python 3.12 version
RUN pip3.12 install -r requirements.txt

# now also install docker-compose in the 'builder' stage
# this ensure docker-compose is available when the Docker image is built
RUN apt-get update && \
    apt-get install -y docker-compose


# 'app' stage—this contains the final application image
# Updated Python version to 3.12
FROM python:3.12-slim as app

# Setting the environment path for Python 3.12
ENV PATH="/opt/python/bin:${PATH}"
ENV PYTHON="/opt/python/bin/python3.12"

# Set a working directory for the 'app' stage
WORKDIR /app

# Copy the necessary files from the 'builder' stage to the 'app' stage
# This includes any installed Python packages and the compiled application code
# Modified to copy dependencies assuming Python 3.12 folders/locations
COPY --from=builder /builder/venv/lib/python3.12/site-packages /app/venv/lib/python3.12/site-packages
COPY --from=builder /builder/src /app

# Expose the port where the app is running
EXPOSE 8080

# Run the app with python3.12 executable
CMD ["python3.12", "app.py"]

# End of Dockerfile