```Dockerfile
# Python image to use as a base
FROM python:3.9-slim as builder

# Add Python to path and set python version
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.9"

# Setting the workdir to /builder
WORKDIR /builder

# Copying application requirements and source code to /builder
COPY requirements.txt /builder
COPY src /builder/src

# Install Python packages from requirements.txt without caching
RUN pip3 install --no-cache-dir -r requirements.txt

# Start new stage for the app 
FROM python:3.9-slim as app

# Add Python to path and set python version
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.9"

# Setting the workdir to /app
WORKDIR /app

# Copy Python packages from builder stage and application source code to the app stage
COPY --from=builder /builder/venv/lib/python3.9/site-packages /app/venv/lib/python3.9/site-packages
COPY --from=builder /builder/src /app

# Changes for Kinsta environment
ENV KINSTA_DEPLOYMENT='TRUE'

# Expose a port to allow external access
EXPOSE 8080

# The command that will be run on container start
CMD ["python3.9", "app.py", "--kinsta"]
```