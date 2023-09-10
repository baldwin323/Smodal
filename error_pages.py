from django.shortcuts import render

# Create your views here.
# Custom 404 error page for Replit
def handler404(request, exception):
    # Render the '404.html' template and return an HTTP response with status code 404.
    content = {
        'error_code': '404', 
        'error_message': 'Page Not Found'
    }
    return render(request, '404.html', content, status=404)

# Custom 500 error page for Replit
def handler500(request):
    # Render the '500.html' template and return an HTTP response with status code 500.
    content = {
        'error_code': '500', 
        'error_message': 'Internal Server Error'
    }
    return render(request, '500.html', content, status=500)