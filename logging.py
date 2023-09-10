import logging
import os

# This script is for logging purposes for our application.
# It includes both console logging and file logging.
# Console logging is set to level INFO, which means it will record every detail at or above INFO level (DEBUG < INFO < WARNING < ERROR < CRITICAL)
# File logging is set to level ERROR, which means it will record only ERROR and CRITICAL level details.

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers for console and file
console_handler = logging.StreamHandler()
if os.getenv('REPLIT') == '1':
  filename = 'replit_app.log'
else:
  filename = 'app.log'
file_handler = logging.FileHandler(filename)

# We set the level of logging for console and file
# console logging is lowered to INFO level,
# whereas file logging is kept at ERROR level.
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.ERROR)

# Create formatters to specify the format of log message and add these formatters to the handlers 
# Console formatter does not have timestamp information and it only logs name of the logger, level of logging and the message
# File formatter logs more about the error, including timestamp, name of the logger, level of logging, message, pathname of the module where error occurred and the line number of the code where error occurred
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - line %(lineno)d')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Finally, we add these handlers to our logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)