import logging

from pydantic.error_wrappers import ErrorWrapper, ValidationError
from Smodal.models import UserProfileModel, FileUploadModel, BankingModel, AIConversationModel, UIPageDataModel

# Import the logging module to allow logging of exceptions
logger = logging.getLogger(__name__)

class ErrorDetails:
    '''
    A class to handle HTTP errors
    Contains properties for HTTP status code and appropriate HTML template
    Also have a property to handle API related errors
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

    if isinstance(exception, (ErrorWrapper, ValidationError)):
        # Pydantic model related errors are handled here
        logger.error(f'HTTP {error_code}: {str(exception)}, Error: {error_message}')
    else if error_code == 500:
        logger.error(f'HTTP {error_code}: Unhandled exception, Error: {error_message}')

    return error_code, error_message

def error_handler(exception, error_code):
    '''
    A function to handle HTTP errors
    Returns HTTP status code and error message
    Note: Unlike Django, Pydantic errors don't involve rendering HTML templates
    '''

    error_code, error_message = handle_exception(exception, error_code)
    if 'API' in str(exception):
        error_message = f"API Error: {str(exception)}"
        logger.error(f'API Error, Error: {error_message}')

    return {
        'error_code': error_code,
        'error_message': error_message,
    }


def handler400(exception=None):
    '''
    Function to handle 400 error,
    calls error_handler with 400 code
    and handles the logging
    '''
    return error_handler(exception, 400)


def handler404(exception=None):
    '''
    Function to handle 404 error,
    calls error_handler with 404 code
    and handles the logging
    '''
    return error_handler(exception, 404)


def handler500(exception=None):
    ''' 
    Function to handle 500 error,
    calls error_handler with 500 code
    and handles the logging
    '''
    return error_handler(exception, 500)