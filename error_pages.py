from django.shortcuts import render

# Create your views here.
# The purpose of this is to redirect to a custom 404 error page when the server cannot find the requested URL
def handler404(request, exception):
    # It renders a '404.html' template and returns an HTTP response with status code 404.
    return render(request, '404.html', {}, status=404)

# This function is to redirect to a custom 500 error page when the server encounters an internal error.
def handler500(request):
    # It renders a '500.html' template and returns an HTTP response with status code 500.
    return render(request, '500.html', {}, status=500)