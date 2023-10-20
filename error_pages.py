import logging

from django.shortcuts import render
from django.http.response import Http404, BadRequest, HttpResponseServerError

# Import the logging module to allow logging of exceptions
logger = logging.getLogger(__name__)

class ErrorDetails:
    '''
    A class to handle HTTP errors
    Contains properties for HTTP status code and appropriate HTML template
    '''
    def __init__(self, code, message):
        self.code = code
        self.message = message

error_details = {
    400: ErrorDetails(400, "Bad Request. The server could not understand the request."),
    404: ErrorDetails(404, "Page Not Found. The resource requested could not be found on the server."),
    500: ErrorDetails(500, "Internal Server Error. The server encountered an unexpected condition."),
}

def handle_exception(exception, error_code):
    error_detail = error_details.get(error_code)
    error_message = error_detail.message if error_detail else "Unknown Error"

    if isinstance(exception, (BadRequest, Http404)) or error_code == 500:
        logger.error(f'HTTP {error_code}: {str(exception)}, Error: {error_message}')

    return error_code, error_message

def error_handler(request, exception, error_code):
    '''
    A function to handle HTTP errors
    Returns HTTP status code and renders appropriate HTML template
    Error message also logged with logger
    '''
    
    error_code, error_message = handle_exception(exception, error_code)
    
    context = {
        'error_code': error_code, 
        'error_message': error_message,
    }

    return render(request, f'error/{error_code}.html', context, status=error_code)


def handler400(request, exception=None):
    '''
    Function to handle 400 error, 
    calls error_handler with 400 code
    and handles the logging
    '''
    return error_handler(request, exception, 400)


def handler404(request, exception=None):
    '''
    Function to handle 404 error, 
    calls error_handler with 404 code
    and handles the logging
    '''
    return error_handler(request, exception, 404)


def handler500(request, exception=None):
    ''' 
    Function to handle 500 error, 
    calls error_handler with 500 code
    and handles the logging
    '''
    return error_handler(request, exception, 500)