import logging
import os

# Modified script for logging purposes of the application.
# It includes both console logging and file logging.
# Console logging is set to level INFO, which includes every detail at or above INFO level (DEBUG < INFO < WARNING < ERROR < CRITICAL)
# File logging is set to level ERROR, which only includes ERROR and CRITICAL level details.

# Creating a custom logger
logger = logging.getLogger(__name__)

# Create handlers for console and file logging
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

# Set the level of logging for console and file.
# Console logging includes all details from INFO level.
# File logging includes only ERROR and CRITICAL level details.
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.ERROR)

# Create formatters to specify the format of log message and associate these formatters to the respective handlers.
# Console formatter maintains information of logger name, level of logging and the message.
# File formatter maintains additional information about the error including timestamp, pathname of the module where the error occurred and the line number of the code where the error occurred.
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - line %(lineno)d')

# Set the Formatter for console and file handler.
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add these handlers to the custom logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)