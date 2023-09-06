# Import necessary modules
from django.shortcuts import render
from django.urls import path

def navbar_view(request):
    """Render the Navbar HTML template"""
    return render(request, 'navbar.html', {}) 

def footer_view(request):
    """Render the Footer HTML template"""
    return render(request, 'footer.html', {}) 

def modal_view(request):
    """Render the Modal HTML template"""
    return render(request, 'modal.html', {}) 

def other_page_view(request):
    """Render other HTML templates"""
    return render(request, 'other_page.html', {}) 

# Register the URL patterns
urlpatterns = [
    path('navbar', navbar_view, name='navbar-url-name'),
    path('footer', footer_view, name='footer-url-name'),
    path('modal', modal_view, name='modal-url-name'),
    path('other_page', other_page_view, name='other-page-url-name'),
]  

# Django template language files

# Navbar Template
'''
<!DOCTYPE html>
<html>
<head>
    {% load static %}
    <title>Navbar</title>
    <link href="{% static 'css/navbar.css' %}" rel="stylesheet">
</head>
<body>
    <script src="{% static 'js/navbar.js' %}"></script>
</body>
</html>
'''

# Footer Template
'''
<!DOCTYPE html>
<html>
<head>
    {% load static %}
    <title>Footer</title>
    <link href="{% static 'css/footer.css' %}" rel="stylesheet">
</head>
<body>
    <script src="{% static 'js/footer.js' %}"></script>
</body>
</html>
'''

# Modal Template
'''
<!DOCTYPE html>
<html>
<head>
    {% load static %}
    <title>Modal</title>
    <link href="{% static 'css/modal.css' %}" rel="stylesheet">
</head>
<body>
    <script src="{% static 'js/modal.js' %}"></script>
</body>
</html>
'''

# Other Page Template
'''
<!DOCTYPE html>
<html>
<head>
    {% load static %}
    <title>Other Page</title>
    <link href="{% static 'css/other_page.css' %}" rel="stylesheet">
</head>
<body>
    <script src="{% static 'js/other_page.js' %}"></script>
</body>
</html>
'''