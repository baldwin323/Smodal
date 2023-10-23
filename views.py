import logging
from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, ManagedModels
import requests
import json
# Add missing handler import to solve error 2
from django.views.debug import ExceptionReporter, get_exception_reporter_filter

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
    'affiliate_manager': {
        'method': lambda req: load_template('affiliate_manager.html'),
        'login_required': True
    },
    'new_feature': {
        'method': lambda req: load_template('new_feature.html'),
        'login_required': True
    },
    'another_new_feature': {
        'method': lambda req: load_template('another_new_feature.html'),
        'login_required': True
    }
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
    return redirect('index')

@require_login
def form_submit(request):
    # Check for circular imports related issues 
    # process form
    return load_template('result.html')

def login(request):
    if is_authenticated(request):
        return redirect('index')
    if request.method == 'POST':
        # Update login form processing methodology
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
            return redirect('login')
        return page_cfg['method'](request)
    else:
        return Http404

def serve(request, page):
    return render(request, page)

@require_login
def register_affiliate_manager(request):
    if request.method == 'POST':
        # Code to register a new affiliate manager goes here
        pass
    return render(request, 'register_affiliate_manager.html')

@require_login
def list_affiliated_models(request, manager_id):
    models = ManagedModels.objects.filter(manager__id=manager_id)
    return render(request, 'affiliated_models.html', {'models': models})

@require_login
def give_credit(request, model_id):
    model = ManagedModels.objects.get(id=model_id)
    if model.referral:
        # Give a referral credit to the affiliate manager
        model.referral.credits += 1
        model.referral.save()
    return JsonResponse({'success': True}, status=200)

@require_login
def new_feature(request):
    return render(request, 'new_feature.html')

@require_login
def another_new_feature(request):
    return render(request, 'another_new_feature.html')