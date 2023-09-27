from django.shortcuts import render
from django.urls import path, include

def render_html_template(request, template_name, context={}):
    """Render any HTML template"""
    return render(request, template_name, context)

urlpatterns = [
    path('<str:template_name>', render_html_template, name='html-template-url-name'),
]