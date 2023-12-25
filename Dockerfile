# Dockerfile with Python version updated to 3.12

# 'builder' stage -- this is a temporary image used for building our application
FROM python:3.12-slim as builder

# Setting up Python path to Python 3.12 and creating a new work directory
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.12"
WORKDIR /builder

# Copying requirements and source code into the builder
COPY requirements.txt /builder
COPY src /builder/src

# Installing the requirements into the environment
RUN pip3 install --no-cache-dir -r requirements.txt

# 'app' stage -- this contains our final application image
FROM python:3.12-slim as app

# Setting up Python path to Python 3.12 and creating a new work directory
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.12"
WORKDIR /app

# Copying the necessary files from 'builder'
COPY --from=builder /builder/venv/lib/python3.12/site-packages /app/venv/lib/python3.12/site-packages
COPY --from=builder /builder/src /app

# Defining environment variables required for Kinsta deployment
ENV KINSTA_DEPLOYMENT='TRUE'

# The app listens on port 8080 and it should be exposed
EXPOSE 8080

# Specifying the build and run commands
CMD ["python3.12", "app.py", "--kinsta"]