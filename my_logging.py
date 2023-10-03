import os
import my_logging.config
from django.conf import settings

# Using Logstash as a centralized logging system
from logstash_async.handler import AsynchronousLogstashHandler

logger = logging.getLogger(__name__)

host = 'logstash'
port = 5959

# Create Asynchronous Logstash Handler
handler = AsynchronousLogstashHandler(host, port, database_path=None)

# Set handler level
handler.setLevel(logging.INFO)

# Define Logstash Formatter
formatter = logstash.LogstashFormatterV1()

# Set formatter to handler
handler.setFormatter(formatter)

# Add Handler to Logger
logger.addHandler(handler)