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

def title_page_view(request):
    """Render the Title HTML template"""
    return render(request, 'title.html', {})

urlpatterns = [
    path('navbar', navbar_view, name='navbar-url-name'),
    path('footer', footer_view, name='footer-url-name'),
    path('modal', modal_view, name='modal-url-name'),
    path('other_page', other_page_view, name='other-page-url-name'),
    path('title_page', title_page_view, name='title-page-url-name'),
]