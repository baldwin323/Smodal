import logging
from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from . models import OIDCConfiguration, Credentials, APICredentials
import requests
import json

logger = logging.getLogger(__name__)

# Page mapping
PAGES = {
    'index': {
        'method': lambda req: load_template('index.html'),
        'login_required': False
    },
    'login': {
        'method': lambda req: login(req),
        'login_required': False
    },
    'logout': {
        'method': lambda req: logout(req),
        'login_required': True
    },
}

def is_authenticated(request):
    return 'username' in request.session

def require_login(func):
    def func_wrapper(request):
        if is_authenticated(request):
            return func(request)
        return load_template('login.html')
    return func_wrapper

def index(request):
    return load_template('index.html')

@require_login
def logout(request):
    del request.session['username']
    return index(request)
   
@require_login
def form_submit(request):
    # process form
    return load_template('result.html')

def login(request):
    if is_authenticated(request):
        return index(request)
    if request.method == 'POST':
        # process login form
    return load_template('login.html')

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

def render(request, page):
    if page in PAGES:
        page_cfg = PAGES[page]
        if page_cfg.get('login_required', False) and not is_authenticated(request):
            return load_template('login.html')
        return page_cfg['method'](request)
    else:
        return Http404

def serve(request, page):
    return render(request, page)