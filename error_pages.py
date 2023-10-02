from django.shortcuts import render

def error_handler(request, exception=None, error_code=500):
    '''
    A Generic function to handle HTTP errors
    Returns HTTP status code and renders appropriate HTML template
    '''
    error_messages = {
        '400': 'Bad Request',
        '404': 'Page Not Found',
        '500': 'Internal Server Error',
    }

    content = {
        'error_code': error_code, 
        'error_message': error_messages[str(error_code)],
    }

    return render(request, f'error/{error_code}.html', content, status=error_code)

def handler400(request, exception=None):
    '''
    Function to handle 400 error, 
    calls error_handler with 400 code
    '''
    return error_handler(request, exception, 400)

def handler404(request, exception=None):
    '''
    Function to handle 404 error, 
    calls error_handler with 404 code
    '''
    return error_handler(request, exception, 404)

def handler500(request, exception=None):
    ''' 
    Function to handle 500 error, 
    calls error_handler with 500 code
    '''
    return error_handler(request, exception, 500)