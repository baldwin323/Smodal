```Dockerfile
FROM python:3.12-slim as builder
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.12"
WORKDIR /builder
COPY requirements.txt /builder
COPY src /builder/src
RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.12-slim as app
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHON="/usr/local/bin/python3.12"
WORKDIR /app
COPY --from=builder /builder/venv/lib/python3.12/site-packages /app/venv/lib/python3.12/site-packages
COPY --from=builder /builder/src /app
ENV KINSTA_DEPLOYMENT='TRUE'
EXPOSE 8080
CMD ["python3.12", "app.py", "--kinsta"]
```