import logging
from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from . models import OIDCConfiguration, Credentials, APICredentials
from .logging import log_pactflow_response
import requests
import json

logger = logging.getLogger(__name__)

def load_template(template_name):
    return render(template_name)

def serve_page(request, page):
    if page == 'index':
        return index(request)
    elif page == 'login':
        return login(request)
    elif page == 'logout':
        return logout(request)
    else:
        return Http404

def get_interactions():
    # Not applicable here

def render_elements(request, page):
    if page in ['index', 'login', 'logout']:
        return serve_page(request, page)
    else:
        raise Http404

def handle_function(function_name, *args, **kwargs):
    if function_name == 'index':
        return index(*args, **kwargs)
    elif function_name == 'form_submit':
        return form_submit(*args, **kwargs)
    elif function_name == 'login':
        return login(*args, **kwargs)
    elif function_name == 'logout':
        return logout(*args, **kwargs)
    elif function_name == 'social_media_login':
        return social_media_login(*args, **kwargs)
    else:
        raise ValueError('Invalid function name')

def index(request):
    return load_template('index.html')

def login(request):
    if 'username' in request.session:
        # user already logged in
        return handle_function('index', request)
    if request.method == 'POST':
        # process login form
    return load_template('login.html')

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return handle_function('index', request)
   
def form_submit(request):
    if request.method == 'POST':
        # process form
    return load_template('result.html')

def social_media_login(request: HttpRequest, platform: str) -> Optional[HttpResponse]:
    try:
        api_keys = APICredentials.objects.filter(platform=platform)
        login_details = None
        if not api_keys.exists():
            login_details = Credentials.objects.filter(platform=platform)
            if not login_details.exists():
                return JsonResponse({"error": f"No login credentials were found for {platform}."}, status=404)
        return JsonResponse({"success": f"Successfully fetched credentials for {platform}."}, status=200)
    except Exception as e:
        logger.error(f"Error fetching credentials for {platform}: {str(e)}", exc_info=True)
        return JsonResponse({"error": f"Could not fetch credentials for {platform} due to {str(e)}."}, status=500)


def oidc_auth(request: HttpRequest) -> Optional[HttpResponse]:
    # OIDC logic

def oidc_callback(request: HttpRequest) -> Optional[HttpResponse]:
    # OIDC callback logic