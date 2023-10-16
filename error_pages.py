import logging

from django.shortcuts import render

# Import the logging module to allow logging of exceptions
logger = logging.getLogger(__name__)

def error_handler(request, exception=None, error_code=500):
    '''
    A Generic function to handle HTTP errors
    Returns HTTP status code and renders appropriate HTML template
    Error message also logged with logger
    '''
    error_messages = {
        '400': 'Bad Request',
        '404': 'Page Not Found',
        '500': 'Internal Server Error',
    }

    if exception:
        if exception.__class__.__name__ == 'ModuleNotFoundError':
            error_message = "Error in module import. Please check the dependencies."
            error_code = 500
        else:
            error_message = error_messages.get(str(error_code), 'Unknown Error')

        # Log the exception if it exists
        logger.error(f'HTTP {error_code}: {str(exception)}, Error: {error_message}')
    else:
        error_message = error_messages.get(str(error_code), 'Unknown Error')
    
    content = {
        'error_code': error_code, 
        'error_message': error_message,
    }

    return render(request, f'error/{error_code}.html', content, status=error_code)


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