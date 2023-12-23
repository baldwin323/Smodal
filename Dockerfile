# Updated Dockerfile for smodal

# 'builder' stage -- this is a temporary image used for building our application
FROM python:3.12-slim as builder

# Setting the environment path for Python 3.12
# Point to the correct python binary location
ENV PATH="/opt/python/bin:${PATH}" 
ENV PYTHON="/opt/python/bin/python3.12"

WORKDIR /builder

# Copies the Python requirements file and the source code; we copy only what we need for this stage
# Instruct COPY to copy to Python 3.12 appropriate locations
COPY requirements.txt /builder
COPY src /builder/src

# Install requirements in the 'builder' stage
# We separate this command because Docker can cache the output to speed up rebuilds
# Adjusted as per Python 3.12 package management
RUN pip3 install -r requirements.txt

# 'app' stage -- this contains our final application image
FROM python:3.12-slim as app

# Setting the environment path for Python 3.12
ENV PATH="/opt/python/bin:${PATH}"
ENV PYTHON="/opt/python/bin/python3.12"

WORKDIR /app

# Copy the necessary files from the 'builder' stage to the 'app' stage
# Adjust the COPY commands to reflect Python 3.12 folder structure
# This includes any installed Python packages and the app code
COPY --from=builder /builder/venv/lib/python3.12/site-packages /app/venv/lib/python3.12/site-packages
COPY --from=builder /builder/src /app

# Defining environment variables required for Kinsta deployment
ENV KINSTA_DEPLOYMENT = 'TRUE'
# Add more environment variables as needed

# Installing packages necessary for Kinsta
# Add package installation commands here as needed

# The app listens on port 8080 and it should be exposed
EXPOSE 8080

# Specifying the build and run commands for Kinsta
CMD ["python3.12", "app.py", "--kinsta"]

# End of Updated Dockerfile