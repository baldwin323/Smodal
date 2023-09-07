# Import necessary modules for rendering templates and constructing URLs
from django.shortcuts import render
from django.urls import path

# Define a function for rendering the navbar HTML template
def navbar_view(request):
    """Render the Navbar HTML template"""
    return render(request, 'navbar.html', {})

# Define a function for rendering the footer HTML template
def footer_view(request):
    """Render the Footer HTML template"""
    return render(request, 'footer.html', {})

# Define a function for rendering the modal HTML template
def modal_view(request):
    """Render the Modal HTML template"""
    return render(request, 'modal.html', {})

# Define a function for rendering other HTML templates
def other_page_view(request):
    """Render other HTML templates"""
    return render(request, 'other_page.html', {})

# Registering the defined URL patterns
# Each URL pattern is associated with their respective view functions
urlpatterns = [
    path('navbar', navbar_view, name='navbar-url-name'),
    path('footer', footer_view, name='footer-url-name'),
    path('modal', modal_view, name='modal-url-name'),
    path('other_page', other_page_view, name='other-page-url-name'),
]  

# Django template language files are used to generate HTML dynamically

# Navbar Template:
# Load the static files for the necessary CSS and JS
# The rendered HTML will incorporate the necessary nav bar elements
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

# Footer Template:
# Load the static files for the necessary CSS and JS
# The rendered HTML will incorporate the necessary footer elements
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

# Modal Template:
# Load the static files for the necessary CSS and JS
# The rendered HTML will incorporate the necessary modal elements
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

# Other Page Template:
# Load the static files for the necessary CSS and JS
# The rendered HTML will correspond to the given other page design
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